# linux_stuff

This repository contains my personal Linux dotfiles, a macOS Bash environment,
and platform-specific installers for configuration and required packages.

It supports:
- Debian/Ubuntu/Mint and other **apt-based** distros via `./install_debian`
- **Gentoo** via `./install_gentoo`
- **macOS** Bash shell environment via `./install_mac`

---

## What’s included

### bash
- aliases (e.g. `ll` for `ls -al`)
- `nano` is aliased to `micro`
- `eza` as `ls` replacement
- console prompt inspired by Kali Linux
- colourful greeting using `fastfetch`, `toilet`, `lolcat`
- Go environment settings

### Midnight Commander (mc)
- lynx-like motion enabled

### nano
- line numbers
- colours
- syntax highlighting

### micro
- crisp high-contrast colour scheme

### alacritty
- dark classic high-contrast theme
- Fira Code font

### herbstluftwm
- desktop background with key bindings displayed
- configurable for small/large screens and different apps
- green focus
- polybar with colourful icons, time and weather display
- switch off laptop screen when a monitor is connected to HDMI-1

#### Important keybindings (some are herbstluftwm defaults)
    win-alt-s           open music player (e.g. spotify)
    win-alt-b           open web browser
    win-alt-n           open file browser (e.g. nemo)
    win-Esc             close current window
    win-, / win-.        navigate through tags (workspaces)
    win-arrows          move focus
    win-shift-arrows    move window
    win-space           open program launcher
    win-shift-q         logout

#### Configuration
See `home/.config/herbstluftwm/autostart` (variables at the top).

### Polybar
- herbstluftwm workspaces
- weather (Lübeck, Germany)
- local date/time
- CPU load, free RAM, core temperature
- audio level
- current IP
- power-off/logout button

Tray applets (not installed by the scripts):
- `blueman-applet` (Bluetooth control)
- `nm-applet` (Wi-Fi network management)

---

## Dependencies

The exact dependency set depends on the target system and install mode.
All installer scripts can print their dependency list:

- apt-based distros:
  - `./install_debian -p`
- Gentoo:
  - `./install_gentoo -p`
- macOS:
  - `./install_mac -p`

Note: On Gentoo, `micro` (and `lolcat`) may require `~amd64` keywords; `install_gentoo`
handles this automatically on amd64.

---

## Installation

### apt-based distros (Debian/Ubuntu/Mint)
Run:
    ./install_debian

It prints usage and the available modes.

### Gentoo
Run:
    ./install_gentoo

It prints usage and the available modes.

### macOS (Bash only)

Requirements: Bash must already be the account's default login shell. The installer
checks the account setting with `dscl` and does not change it. Apple's `/bin/bash`
(3.2) and Homebrew Bash are supported. To select Apple's Bash yourself, use
`chsh -s /bin/bash`, then open a new terminal.

[Homebrew](https://brew.sh/) must already be installed and `brew` must be in PATH.
Run as your regular user:

```sh
./install_mac -p   # list Homebrew dependencies
./install_mac -c   # install dependencies and shell configuration
./install_mac -d   # configuration only; dependencies must already be installed
```

Installs `git`, `curl`, `unzip`, `fastfetch`, `toilet`, `midnight-commander`,
`nano`, `micro`, `eza`, and `lolcat` through Homebrew. Formula availability was
checked in the [official Homebrew catalog](https://formulae.brew.sh/formula/).
No Linux package manager, X11, window manager, Polybar, GUI terminal, or fonts
are installed.

Links the macOS-specific `mac/.bashrc` plus shared `micro` and `mc` settings.
Generates `~/.bash_profile` to initialize the detected Homebrew installation and
load `.bashrc` in interactive login shells. Generates `~/.nanorc` with syntax
paths from the actual Homebrew prefix. Existing profile and editor settings are
backed up before replacement. The macOS Bash configuration keeps the prompt,
eza aliases, greeting, and directory helpers; it uses native macOS `ifconfig`
and excludes Linux paths, GTK settings, and X11 commands.

All installers:
- move existing files and directories into unique backup directories named
  `<destination>_old_<timestamp>.<random>/original`
- preserve earlier backups even when installations share the same timestamp
- replace existing symlinks without backing up the link itself
- link repository configuration into `$HOME` (macOS also generates the two files above)

## Validation and review

Run the non-destructive checks with Python 3:

```sh
python3 -m unittest discover -s tests -v
```

The 15 checks parse shell scripts and exercise the Debian and macOS installers
in isolated temporary homes. macOS package operations and account information
are mocked; Bash startup is exercised with Apple's `/bin/bash`. Tests do not
install packages or start a desktop.
See [REVIEW.md](REVIEW.md) for findings and remaining validation limits.

Gentoo uses `app-misc/fastfetch` for the shell greeting. Dotfile-only installation
(`-d`) does not invoke sudo. The apt terminal mode (`-k`) also installs `eza` and
`lolcat`. Polybar resolves the workspace script relative to the current `$HOME`.

To restore a backup, remove the installed symlink and move the backup directory's
`original` entry back to its original destination. Keep the repository in place:
the installed symlinks point into it.
