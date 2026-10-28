"""Run non-destructive checks without installing packages or starting X11."""
import os
from pathlib import Path
import subprocess
import shlex
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ProjectTests(unittest.TestCase):
    """Check shell syntax and installer behavior in an isolated home."""

    def test_shell_syntax(self):
        """Parse every maintained shell script without executing it."""
        paths = [ROOT / name for name in ('install_debian', 'install_gentoo', 'install_mac', 'cleanup_mac_once', 'mac/.bashrc', 'home/.bashrc',
                                         'home/.config/herbstluftwm/autostart')]
        paths.extend(ROOT.glob('home/.config/**/*.sh'))
        paths.extend(ROOT.glob('tools/*.sh'))
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                subprocess.run(['bash', '-n', str(path)], check=True)

    def test_dotfiles_install_and_repeat(self):
        """Verify backups, symlink targets, and repeated apt dotfile installation."""
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            (home / '.bashrc').write_text('original\n')
            env = dict(os.environ, HOME=directory)
            for _ in range(2):
                subprocess.run(['bash', str(ROOT / 'install_debian'), '-d'], env=env,
                               check=True, capture_output=True, text=True)
            self.assertEqual((home / '.bashrc').resolve(), ROOT / 'home/.bashrc')
            backups = list(home.glob('.bashrc_old_*'))
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / 'original').read_text(), 'original\n')
            for source in (ROOT / 'home/.config').iterdir():
                if source.is_dir():
                    self.assertEqual((home / '.config' / source.name).resolve(), source)

    def test_dependency_listing(self):
        """Print apt dependencies without modifying the host."""
        result = subprocess.run(['bash', str(ROOT / 'install_debian'), '-p'],
                                check=True, capture_output=True, text=True)
        self.assertIn('Dependencies used by this installer', result.stdout)

    def run_functions(self, installer, commands, home):
        """Execute installer helpers without platform checks or package operations."""
        source = (ROOT / installer).read_text().split('# ---------------------- main')[0]
        source = '\n'.join(line for line in source.splitlines()
                           if not line.startswith('SCRIPT_DIR='))
        source = 'SCRIPT_DIR=' + shlex.quote(str(ROOT)) + '\n' + source
        return subprocess.run(['bash', '-c', source + '\n' + commands],
                              env=dict(os.environ, HOME=str(home)), check=True,
                              capture_output=True, text=True)

    def test_backup_collisions(self):
        """Preserve files and directories even when backup timestamps are identical."""
        for installer in ('install_debian', 'install_gentoo'):
            with self.subTest(installer=installer), tempfile.TemporaryDirectory() as d:
                home = Path(d)
                self.run_functions(installer, """
# Return a constant timestamp to force identical backup prefixes.
date() { printf '%s\\n' fixed; }
printf first > "$HOME/item"
create_safelink item "$REPO_SOURCE"
rm "$HOME/item"
printf second > "$HOME/item"
create_safelink item "$REPO_SOURCE"
mkdir "$HOME/folder"
printf first > "$HOME/folder/data"
create_safelink folder "$REPO_SOURCE"
rm "$HOME/folder"
mkdir "$HOME/folder"
printf second > "$HOME/folder/data"
create_safelink folder "$REPO_SOURCE"
""".replace('$REPO_SOURCE', str(ROOT / 'home/.bashrc')), home)
                self.assertEqual(sorted(p.read_text() for p in home.glob('item_old_*/original')),
                                 ['first', 'second'])
                self.assertEqual(sorted(p.read_text() for p in home.glob('folder_old_*/original/data')),
                                 ['first', 'second'])

    def test_gentoo_dotfiles_without_privileges(self):
        """Fail if Gentoo dotfile installation attempts privilege escalation."""
        with tempfile.TemporaryDirectory() as d:
            self.run_functions('install_gentoo', """
# Reject and record every unexpected privileged operation.
run_root() { touch "$HOME/privilege_attempt"; return 1; }
install_dotfiles
""", Path(d))
            self.assertFalse((Path(d) / 'privilege_attempt').exists())
            self.assertEqual((Path(d) / '.bashrc').resolve(), ROOT / 'home/.bashrc')

    def test_terminal_mode_dependencies(self):
        """Exercise terminal mode dispatch with mocked installation operations."""
        with tempfile.TemporaryDirectory() as d:
            result = self.run_functions('install_debian', """
# Replace package operations with observable test doubles.
# Accept the mocked package platform.
is_apt_system() { return 0; }
# Suppress privileged package commands.
sudo() { :; }
# Record font installation.
install_fira_font() { echo fonts; }
# Record eza installation.
install_eza() { echo eza; }
# Record lolcat installation.
install_lolcat() { echo lolcat; }
# Record dotfile installation.
install_dotfiles() { echo dotfiles; }
set -- -k
""" + (ROOT / 'install_debian').read_text().split('# ---------------------- main')[1].split('\n', 1)[1], Path(d))
            for dependency in ('fonts', 'eza', 'lolcat', 'dotfiles'):
                self.assertIn(dependency, result.stdout.splitlines())

    def test_desktop_configuration(self):
        """Check portable workspace paths and the configured mouse modifier."""
        for config in (ROOT / 'home/.config/polybar').glob('config*'):
            self.assertIn('exec = "${env:HOME}/.config/polybar/info-hlwm-workspaces.sh"',
                          config.read_text())
            self.assertNotIn('/home/elsni/', config.read_text())
        autostart = (ROOT / 'home/.config/herbstluftwm/autostart').read_text()
        self.assertNotIn('$Mod-Button', autostart)
        for button in (1, 2, 3):
            self.assertIn(f'hc mousebind $WIN-Button{button}', autostart)

    def test_gentoo_fastfetch_dependency(self):
        """Ensure Gentoo installs the system information command used by bashrc."""
        with tempfile.TemporaryDirectory() as d:
            result = self.run_functions('install_gentoo', 'print_deps', Path(d))
            self.assertIn('app-misc/fastfetch', result.stdout)
            self.assertNotIn('app-misc/neofetch', result.stdout)


if __name__ == '__main__':
    unittest.main()
