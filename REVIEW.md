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

Twenty tests cover shell syntax, isolated dotfile installation and repetition,
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

## Platform installers

- Renamed the Debian entry point to `install_debian`; documentation, usage output,
  and tests use the new name. No legacy wrapper is provided.
- Added `install_mac` with explicit Homebrew console formulas and separate
  macOS Bash settings. Installation requires macOS, a Bash account login shell,
  a regular user, and an existing Homebrew installation.
- Only `.bashrc`, `.bash_profile`, `.nanorc`, micro, and mc configuration are
  installed on macOS. No X11 or desktop configuration is linked.
- Seven additional macOS tests cover package dispatch, backups and repeat runs,
  interactive profile loading, configuration-only mode, rejected platforms and
  zsh accounts, missing Homebrew, dependency listing, and directory navigation.
- Tests use temporary homes and mocked Homebrew/platform commands. The actual
  Apple Bash 3.2 executable parses and exercises the new shell settings on this
  host. Real Homebrew package installation has not been run.

## Homebrew discovery after switching shells

- `install_mac` finds Homebrew in PATH, an explicit `HOMEBREW_PREFIX`, or the
  standard macOS locations, preferring the native architecture.
- `brew shellenv` initializes the installer environment before package operations.
  The same detected absolute path is saved in `.bash_profile` for later logins.
- Added regressions for missing PATH entries, startup from that same environment,
  a custom prefix, and the native prefix order on Apple Silicon and Intel.
- All 18 tests pass; package installation remains mocked and no real dotfiles
  were modified during verification.

## Reuse existing macOS console tools

- macOS console installation checks command availability after Homebrew setup.
  Existing tools from any installation are retained; `midnight-commander` maps
  to the executable `mc`. Only missing commands trigger formula installation.
- Homebrew is still required. Tool versions are not checked.
- `.nanorc` is generated only when Homebrew nano syntax definitions exist;
  otherwise existing nano settings remain untouched. System nano does not
  force an additional Homebrew nano installation.
- All 20 tests pass, including mixed existing/missing commands, no package
  operations when all commands exist, preserved native nano settings, and
  repeated installation after mocked package installation supplies missing tools.

## One-time macOS cleanup

Added `cleanup_mac_once`: preview by default, explicit `--apply` for removal of
redundant git/curl/unzip/nano formulas and neofetch. Installed dependents and nano
syntax references protect existing tools. No autoremove, force, or unrelated
package deletion is performed. Three mocked cleanup tests cover preview,
limited removal, repeated execution, and preservation rules (23 tests total).
Shared macOS account validation and Homebrew discovery now live in
`tools/mac_environment.sh`, used by both macOS scripts.
