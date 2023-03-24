# linux_stuff

Here you find my setup files (dotfile) for a linux environment
of my personal taste.
It works with debian based distros such as:
Debian,(K/L)Ubuntu, Bunsenlabs, DietPi, Raspi OS, Mint ...

it includes configuration for:

## bash
- nice command aliases (like ll for ls -al  etc..)
- exa as ls replacement
- console prompt "borrowed" from Kali Linux
- colourful greeting message with neofetch figlet and lolcat
- golang settings

## Midnight commander
- editor setting (nano)
- lynx-like motion enabled

## nano
- line numbers
- colors
- syntax highlighting

## alacritty
- dark classic high-contrast theme
- Fira Code font

## herbstluftwm
- green focus
- polybar
- switch off laptop screen when a monitor is connected to HDMI-1
### important keybindings (not all are customized)
	win-alt-s        open spotify
	win-alt-b        open Brave Browser
	win-Esc          close current window
    win-, and  win-. navigate through tags (workspaces)
	win-arrows       move window focus to next window
	win-shift-arrows move window
    win-space        open launcher
    win-shift-q      logout

## Polybar
- displays herbsluftwm workspaces
- displays weather for Lübeck/Germany
- displays local date/time
- displays CPU-load, free RAM and core Temp.
- displays current audio level
- displays current IP
- Power-Off/logout button

in Tray:
- blueman-applet (Bluetooth control)
- nm-applet (wifi network connection management)

# Dependencies
You need to have the following packets installed:
- nano
- mc (Midnight Commande)
- neofetch
- exa
- herbstluftwm
- alacritty
- lolcat
- figlet
- polybar

# Font-Dependencies
- Fira Code Font
- Noto Sans (preinstalled on linux Mint)
- Noto Sans Symbols2 (preinstalled on linux Mint)
- Noto Color Emoji (preinstalled on linux Mint)

# Installation
There is an installer script which is able to install the needed dependencies and installs the dotfiles.

	./install

without any parameters it prints the usage.

The install script basically installs the dependencies on ubuntu/debian based systens and 
renames old dotfiles and symlinks to the ones from this package.
If you are not on a debian-based distro you need to install the deendencies yourself and invoke the installer with
	./install -d
to symlink the dotfiles only.
