"""Check the one-shot cleanup without uninstalling actual software."""
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CleanupTests(unittest.TestCase):
    """Exercise exact removal scope and protection rules with mocked Homebrew."""

    def setUp(self):
        """Prepare isolated installation records, configuration, and command log."""
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.installed = self.home / 'installed'
        self.installed.write_text('git\ncurl\nunzip\nnano\nneofetch\neza\n')
        self.log = self.home / 'removed'
        self.brew = self.home / 'brew'
        self.brew.write_text('''#!/bin/bash
case "$1" in
list) cat "$HOME/installed" ;;
--prefix) echo /test/homebrew ;;
uses) [[ "${!#}" != "$TEST_DEPENDENCY" ]] || echo other-tool ;;
uninstall)
  [[ "$HOMEBREW_NO_AUTOREMOVE" == 1 ]] || exit 1
  shift 2
  printf '%s\\n' "$@" >> "$HOME/removed"
  for package in "$@"; do
    grep -Fxv "$package" "$HOME/installed" > "$HOME/next"
    mv "$HOME/next" "$HOME/installed"
  done ;;
*) exit 1 ;;
esac
''')
        self.brew.chmod(0o755)
        self.env = dict(os.environ, HOME=str(self.home), TEST_DEPENDENCY='')

    def run_cleanup(self, apply=False):
        """Run cleanup helpers with a fake Homebrew executable and real system paths."""
        source = (ROOT / 'cleanup_mac_once').read_text().split('# ---------------------- main')[0]
        source = '\n'.join(line for line in source.splitlines()
                           if not line.startswith('SCRIPT_DIR='))
        script = ('SCRIPT_DIR=' + shlex.quote(str(ROOT)) + '\n' + source +
                  '\nBREW_COMMAND=' + shlex.quote(str(self.brew)) +
                  '\ncleanup_formulas' + (' --apply' if apply else ''))
        return subprocess.run(['/bin/bash', '-c', script], env=self.env,
                              capture_output=True, text=True, check=True)

    def test_preview_does_not_uninstall(self):
        """List candidates without modifying package records by default."""
        result = self.run_cleanup()
        self.assertIn('Remove: neofetch', result.stdout)
        self.assertFalse(self.log.exists())
        self.assertIn('git', self.installed.read_text())

    def test_apply_exact_targets_and_repeat(self):
        """Remove only listed duplicate formulas and neofetch, and allow reruns."""
        self.run_cleanup(apply=True)
        expected = [name for name in ('git', 'curl', 'unzip', 'nano')
                    if Path('/usr/bin', name).is_file()] + ['neofetch']
        self.assertEqual(self.log.read_text().splitlines(), expected)
        self.assertIn('eza', self.installed.read_text())
        self.run_cleanup(apply=True)
        self.assertEqual(self.log.read_text().splitlines(), expected)

    def test_preserve_dependents_and_nano_configuration(self):
        """Keep a required formula and nano syntax referenced by existing settings."""
        self.env['TEST_DEPENDENCY'] = 'git'
        (self.home / '.nanorc').write_text('include "/test/homebrew/share/nano/*.nanorc"')
        result = self.run_cleanup(apply=True)
        self.assertIn('Keep git: required by', result.stdout)
        self.assertIn('Keep nano:', result.stdout)
        self.assertNotIn('git', self.log.read_text().splitlines())
        self.assertNotIn('nano', self.log.read_text().splitlines())
        self.assertIn('neofetch', self.log.read_text().splitlines())


if __name__ == '__main__':
    unittest.main()
