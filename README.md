# linux_stuff

This repository contains my personal Linux dotfiles and a small installer that
symlinks them into `$HOME` and (optionally) installs required packages.

It supports:
- Debian/Ubuntu/Mint and other **apt-based** distros via `./install`
- **Gentoo** via `./install_gentoo`

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
Both installer scripts can print their dependency list:

- apt-based distros:
  - `./install -p`
- Gentoo:
  - `./install_gentoo -p`

Note: On Gentoo, `micro` (and `lolcat`) may require `~amd64` keywords; `install_gentoo`
handles this automatically on amd64.

---

## Installation

### apt-based distros (Debian/Ubuntu/Mint)
Run:
    ./install

It prints usage and the available modes.

### Gentoo
Run:
    ./install_gentoo

It prints usage and the available modes.

Both installers:
- move existing files and directories into unique backup directories named
  `<destination>_old_<timestamp>.<random>/original`
- preserve earlier backups even when installations share the same timestamp
- replace existing symlinks without backing up the link itself
- create symlinks from this repository into your `$HOME`

## Validation and review

Run the non-destructive checks with Python 3:

```sh
python3 -m unittest discover -s tests -v
```

The checks parse shell scripts and exercise the apt installer's dotfile mode in
an isolated temporary home. They do not install packages or start a desktop.
See [REVIEW.md](REVIEW.md) for findings and remaining validation limits.

Gentoo uses `app-misc/fastfetch` for the shell greeting. Dotfile-only installation
(`-d`) does not invoke sudo. The apt terminal mode (`-k`) also installs `eza` and
`lolcat`. Polybar resolves the workspace script relative to the current `$HOME`.

To restore a backup, remove the installed symlink and move the backup directory's
`original` entry back to its original destination. Keep the repository in place:
the installed symlinks point into it.
