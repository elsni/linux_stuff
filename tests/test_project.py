"""Run non-destructive checks without installing packages or starting X11."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ProjectTests(unittest.TestCase):
    """Check shell syntax and installer behavior in an isolated home."""

    def test_shell_syntax(self):
        """Parse every maintained shell script without executing it."""
        paths = [ROOT / name for name in ('install', 'install_gentoo', 'home/.bashrc',
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
                subprocess.run(['bash', str(ROOT / 'install'), '-d'], env=env,
                               check=True, capture_output=True, text=True)
            self.assertEqual((home / '.bashrc').resolve(), ROOT / 'home/.bashrc')
            backups = list(home.glob('.bashrc_old_*'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), 'original\n')
            for source in (ROOT / 'home/.config').iterdir():
                if source.is_dir():
                    self.assertEqual((home / '.config' / source.name).resolve(), source)

    def test_dependency_listing(self):
        """Print apt dependencies without modifying the host."""
        result = subprocess.run(['bash', str(ROOT / 'install'), '-p'],
                                check=True, capture_output=True, text=True)
        self.assertIn('Dependencies used by this installer', result.stdout)


if __name__ == '__main__':
    unittest.main()
