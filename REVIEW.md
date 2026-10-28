# Project review — 2026-10-28

## Resolved findings

1. **Backup collisions:** both installers share `tools/install_helpers.sh`.
   `mktemp -d` reserves a unique backup directory; the previous destination is
   moved into its `original` entry. Equal timestamps cannot overwrite earlier
   backups. Existing symlinks are still replaced directly.
2. **Gentoo greeting:** console dependencies now include `app-misc/fastfetch`
   instead of neofetch, matching `.bashrc`.
3. **Terminal dependencies:** apt mode `-k` now installs eza and lolcat.
4. **Workspace module:** all three Polybar configurations use `${env:HOME}`
   instead of `/home/elsni`.
5. **Mouse bindings:** use the configured `$WIN` modifier.
6. **Unnecessary privileges:** Gentoo dotfile linking no longer invokes
   `run_root true`.

## Validation and limits

Run `python3 -m unittest discover -s tests -v`.

Eight tests cover shell syntax, isolated dotfile installation and repetition,
file and directory backups with identical timestamps in both installers,
Gentoo dotfile installation without privilege operations, mocked apt terminal
mode dispatch, desktop configuration, and the fastfetch package declaration.

Package installation and live X11/Polybar behavior have not been exercised.
The fastfetch atom was verified against the official Gentoo package directory:
https://packages.gentoo.org/packages/app-misc/fastfetch

Installer functions and the shared helper have English documentation comments.
Changed source files are below 500 lines. The pre-existing bundled third-party
micro filemanager plugin remains 1,366 lines; splitting that dependency and
reviewing its functions are outside these six installer/configuration fixes.
