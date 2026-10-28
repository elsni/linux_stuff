"""Exercise the macOS installer with isolated accounts and mocked Homebrew."""
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MacTests(unittest.TestCase):
    """Verify shell-only installation without changing the actual user home."""

    def setUp(self):
        """Create a temporary home and deterministic platform/package commands."""
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.home = self.base / 'home'
        self.home.mkdir()
        self.bin = self.base / 'bin'
        self.bin.mkdir()
        self.prefix = self.base / 'brew prefix'
        (self.prefix / 'share/nano').mkdir(parents=True)
        self.env = dict(os.environ, HOME=str(self.home),
                        PATH=str(self.bin) + ':' + os.environ['PATH'],
                        MAC_TEST_PREFIX=str(self.prefix), MAC_TEST_SHELL='/bin/bash',
                        MAC_TEST_PLATFORM='Darwin', MAC_TEST_LOG=str(self.base / 'brew.log'))
        self.command('uname', 'echo "$MAC_TEST_PLATFORM"')
        self.command('dscl', 'echo "UserShell: $MAC_TEST_SHELL"')
        self.command('brew', '''case "$1" in
--prefix) printf '%s\\n' "$MAC_TEST_PREFIX" ;;
shellenv) echo 'export MAC_TEST_BREW_LOADED=yes' ;;
install) printf '%s\\n' "$@" >> "$MAC_TEST_LOG" ;;
*) exit 1 ;;
esac''')
        for name in ('fastfetch', 'toilet', 'lolcat'):
            self.command(name, ':')

    def command(self, name, body):
        """Create an executable test double in the temporary command path."""
        path = self.bin / name
        path.write_text('#!/bin/bash\n' + body + '\n')
        path.chmod(0o755)

    def run_installer(self, mode):
        """Run the real entry point with the isolated environment."""
        return subprocess.run(['/bin/bash', str(ROOT / 'install_mac'), mode],
                              env=self.env, capture_output=True, text=True)

    def require_regular_user(self):
        """Skip successful account installation when the test runner is root."""
        if os.geteuid() == 0:
            self.skipTest('Installer intentionally rejects root accounts')

    def test_install_shell_only_and_preserve_settings(self):
        """Install supported console packages and preserve existing user files."""
        self.require_regular_user()
        for name in ('.bashrc', '.bash_profile', '.nanorc'):
            (self.home / name).write_text('previous ' + name)
        for _ in range(2):
            result = self.run_installer('-c')
            self.assertEqual(result.returncode, 0, result.stderr)
        for name in ('.bashrc', '.bash_profile', '.nanorc'):
            saved = list(self.home.glob(name + '_old_*/original'))
            self.assertIn('previous ' + name, [p.read_text() for p in saved])
        self.assertEqual((self.home / '.bashrc').resolve(), ROOT / 'mac/.bashrc')
        self.assertEqual(sorted(p.name for p in (self.home / '.config').iterdir()),
                         ['mc', 'micro'])
        self.assertFalse((self.home / '.Xresources').exists())
        packages = (self.base / 'brew.log').read_text().splitlines()
        self.assertEqual(packages, ['install', 'git', 'curl', 'unzip', 'fastfetch',
                                    'toilet', 'midnight-commander', 'nano', 'micro',
                                    'eza', 'lolcat'] * 2)
        self.assertIn(str(self.prefix / 'share/nano/*.nanorc'),
                      (self.home / '.nanorc').read_text())
        startup = subprocess.run(['/bin/bash', '--noprofile', '--norc', '-ic',
                                  'source "$HOME/.bash_profile"; '
                                  'test "$MAC_TEST_BREW_LOADED" = yes || exit 1; alias ll'],
                                 env=self.env, capture_output=True, text=True)
        self.assertEqual(startup.returncode, 0, startup.stderr)
        self.assertIn('eza', startup.stdout)
        self.assertNotIn('command not found', startup.stderr)

    def test_dotfiles_only(self):
        """Install configuration without asking Homebrew to install packages."""
        self.require_regular_user()
        result = self.run_installer('-d')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.base / 'brew.log').exists())

    def test_reject_zsh_before_changes(self):
        """Reject accounts whose configured default shell is zsh."""
        self.require_regular_user()
        self.env['MAC_TEST_SHELL'] = '/bin/zsh'
        result = self.run_installer('-c')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Bash must be your default', result.stderr)
        self.assertEqual(list(self.home.iterdir()), [])
        self.assertFalse((self.base / 'brew.log').exists())

    def test_reject_linux_before_changes(self):
        """Reject non-macOS systems before installing packages or dotfiles."""
        self.env['MAC_TEST_PLATFORM'] = 'Linux'
        result = self.run_installer('-c')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('requires macOS', result.stderr)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_missing_homebrew(self):
        """Require Homebrew explicitly rather than downloading it automatically."""
        self.require_regular_user()
        (self.bin / 'brew').unlink()
        self.env['PATH'] = str(self.bin) + ':/usr/bin:/bin'
        result = self.run_installer('-c')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Install Homebrew', result.stderr)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_print_dependencies_without_platform_requirements(self):
        """List dependencies without checking or modifying the account."""
        self.env['MAC_TEST_PLATFORM'] = 'Linux'
        result = self.run_installer('-p')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('fastfetch', result.stdout.splitlines())
        self.assertFalse((self.base / 'brew.log').exists())

    def test_directory_helpers(self):
        """Check native directory navigation and reject invalid level arguments."""
        folder = self.home / 'outer' / 'inner'
        folder.mkdir(parents=True)
        script = ('source ' + shlex.quote(str(ROOT / 'mac/.bashrc')) + '; '
                  'cd "$HOME/outer/inner"; up 2; '
                  'test "$PWD" = "$HOME" || exit 1; '
                  'if up invalid; then exit 1; fi; '
                  'cl; test "$PWD" = "$HOME/outer"')
        result = subprocess.run(['/bin/bash', '--noprofile', '--norc', '-ic', script],
                                env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
