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
- colourful greeting using `neofetch`, `toilet`, `lolcat`
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
- back up existing dotfiles by renaming them with a timestamp suffix
- create symlinks from this repository into your `$HOME`
