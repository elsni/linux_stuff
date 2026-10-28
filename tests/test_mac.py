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
                        PATH=str(self.bin) + ':/usr/bin:/bin',
                        HOMEBREW_PREFIX='', MAC_TEST_PREFIX=str(self.prefix), MAC_TEST_SHELL='/bin/bash',
                        MAC_TEST_BIN=str(self.bin), MAC_TEST_PLATFORM='Darwin', MAC_TEST_LOG=str(self.base / 'brew.log'))
        self.command('uname', 'echo "$MAC_TEST_PLATFORM"')
        self.command('dscl', 'echo "UserShell: $MAC_TEST_SHELL"')
        self.command('brew', '''case "$1" in
--prefix) printf '%s\\n' "$MAC_TEST_PREFIX" ;;
shellenv) printf 'export MAC_TEST_BREW_LOADED=yes; export PATH=%q:$PATH\\n' "$(dirname "$0")" ;;
install)
  printf '%s\\n' "$@" >> "$MAC_TEST_LOG"
  shift
  for package in "$@"; do
    executable="$package"
    [[ "$package" != midnight-commander ]] || executable=mc
    printf '#!/bin/bash\\n:\\n' > "$MAC_TEST_BIN/$executable"
    chmod +x "$MAC_TEST_BIN/$executable"
  done
  ;;
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
        source, main = (ROOT / 'install_mac').read_text().split(
            '# ---------------------- main', 1)
        source = '\n'.join(line for line in source.splitlines()
                           if not line.startswith('SCRIPT_DIR='))
        # Keep standard-prefix discovery isolated from actual host installations.
        script = ('SCRIPT_DIR=' + shlex.quote(str(ROOT)) + '\n' + source +
                  '\n# Print isolated Homebrew locations for this test account.\n'
                  'homebrew_locations() { printf "%s\\n" "$MAC_TEST_PREFIX/bin/brew"; }\n'
                  'set -- ' + shlex.quote(mode) + '\n' + main.split('\n', 1)[1])
        return subprocess.run(['/bin/bash', '-c', script], env=self.env,
                              capture_output=True, text=True)

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
        self.assertEqual(packages, ['install', 'midnight-commander', 'micro', 'eza'])
        self.assertIn(str(self.prefix / 'share/nano/*.nanorc'),
                      (self.home / '.nanorc').read_text())
        startup = subprocess.run(['/bin/bash', '--noprofile', '--norc', '-ic',
                                  'source "$HOME/.bash_profile"; '
                                  'test "$MAC_TEST_BREW_LOADED" = yes || exit 1; alias ll'],
                                 env=self.env, capture_output=True, text=True)
        self.assertEqual(startup.returncode, 0, startup.stderr)
        self.assertIn('eza', startup.stdout)
        self.assertNotIn('command not found', startup.stderr)

    def test_existing_external_commands_skip_homebrew(self):
        """Keep commands from other installations, including mc, without brew install."""
        self.require_regular_user()
        for name in ('git', 'curl', 'unzip', 'mc', 'nano', 'micro', 'eza'):
            self.command(name, ':')
        (self.prefix / 'share/nano').rmdir()
        (self.home / '.nanorc').write_text('existing native nano settings')
        result = self.run_installer('-c')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.base / 'brew.log').exists())
        self.assertIn('Already available: git', result.stdout)
        self.assertIn('Already available: mc (skipping midnight-commander)', result.stdout)
        self.assertEqual((self.home / '.nanorc').read_text(), 'existing native nano settings')
        self.assertEqual(list(self.home.glob('.nanorc_old_*')), [])

    def test_missing_command_installs_only_its_formula(self):
        """Install only the missing mapped formula while keeping all other tools."""
        self.require_regular_user()
        for name in ('git', 'curl', 'unzip', 'nano', 'micro', 'eza'):
            self.command(name, ':')
        result = self.run_installer('-c')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.base / 'brew.log').read_text().splitlines(),
                         ['install', 'midnight-commander'])

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

    def test_homebrew_outside_path(self):
        """Discover Homebrew after switching from zsh and initialize later Bash logins."""
        self.require_regular_user()
        (self.prefix / 'bin').mkdir()
        (self.bin / 'brew').rename(self.prefix / 'bin/brew')
        result = self.run_installer('-c')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.base / 'brew.log').exists())
        profile = (self.home / '.bash_profile').read_text()
        self.assertIn(str(self.prefix / 'bin/brew'), profile.replace('\\', ''))
        startup = subprocess.run(['/bin/bash', '--noprofile', '--norc', '-ic',
                                  'source "$HOME/.bash_profile"; '
                                  'test "$MAC_TEST_BREW_LOADED" = yes || exit 1; '
                                  'command -v brew'], env=self.env,
                                 capture_output=True, text=True)
        self.assertEqual(startup.returncode, 0, startup.stderr)
        self.assertIn(str(self.prefix / 'bin/brew'), startup.stdout)

    def test_native_homebrew_location_order(self):
        """Prefer the native standard prefix on Apple Silicon and Intel Macs."""
        source = (ROOT / 'install_mac').read_text().split('# ---------------------- main')[0]
        source = '\n'.join(line for line in source.splitlines()
                           if not line.startswith('SCRIPT_DIR='))
        for architecture, expected in (
                ('arm64', ['/opt/homebrew/bin/brew', '/usr/local/bin/brew']),
                ('x86_64', ['/usr/local/bin/brew', '/opt/homebrew/bin/brew'])):
            with self.subTest(architecture=architecture):
                script = ('SCRIPT_DIR=' + shlex.quote(str(ROOT)) + '\n' + source +
                          '\n# Report the architecture under test.\n'
                          'uname() { echo ' + architecture + '; }\nhomebrew_locations')
                result = subprocess.run(['/bin/bash', '-c', script], env=self.env,
                                        capture_output=True, text=True, check=True)
                self.assertEqual(result.stdout.splitlines(), expected)

    def test_custom_homebrew_prefix(self):
        """Honor an explicit custom prefix when brew is absent from PATH."""
        self.require_regular_user()
        custom = self.base / 'custom brew'
        (custom / 'bin').mkdir(parents=True)
        (self.bin / 'brew').rename(custom / 'bin/brew')
        self.env['HOMEBREW_PREFIX'] = str(custom)
        result = self.run_installer('-d')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(custom / 'bin/brew'),
                      (self.home / '.bash_profile').read_text().replace('\\', ''))

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
