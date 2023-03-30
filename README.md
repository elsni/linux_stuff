# linux_stuff

Here you find my setup files (dotfile) for a linux environment
of my personal taste.
It works with debian based distros such as:
Debian,(K/L)Ubuntu, Bunsenlabs, DietPi, Raspi OS, Mint ...

it includes configuration for:

## bash
- nice command aliases (like ll for ls -al  etc..)
- 'nano' is alias for mirco
- exa as ls replacement
- console prompt "borrowed" from Kali Linux
- colourful greeting message with neofetch figlet and lolcat
- golang settings

## Midnight commander
- lynx-like motion enabled

## nano
- line numbers
- colors
- syntax highlighting

## micro
- crisp high-contrast color scheme

## alacritty
- dark classic high-contrast theme
- Fira Code font

## herbstluftwm
- configurable for small/large screens and different apps
- green focus
- polybar
- switch off laptop screen when a monitor is connected to HDMI-1
### important keybindings (some are herbstluft-default)
	win-alt-s        open music player (i.e. spotify)
	win-alt-b        open web browser
	win-alt-n        open file browser (i.e. nemo)
	win-Esc          close current window
    win-, and  win-. navigate through tags (workspaces)
	win-arrows       move window focus to next window
	win-shift-arrows move window
    win-space        open program launcher
    win-shift-q      logout

### Configuration
look at home/.config/herbstluftwm/autostart
at the top of the file you can set some variables
to your needs.

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

## Terminal 
- nano - a lightweight console text editor wih syntax highlighting
- mc (Midnight Commande) console mased file manager
- neofetch - nice looking system info dislay
- exa - ls in full color
- lolcat - makes text rainbow-color
- figlet - prints large text on console with ascii characters
- micro editor (https://micro-editor.github.io/)

## X/GUI/Graphical
- herbstluftwm  - a nice tiling window manager
- alacritty - hardware acelerated terminal emualator
- polybar - the info bar and tray 
- ssh-askpass - provides graphical password input for sudo
- lxappearance - GTK-Theme Selection
- pavucontrol - soundcard loudness setting dialog

# Font-Dependencies
- Fira Code Font
- font-awesome (free)
- Noto Sans (preinstalled on linux Mint)
- Noto Sans Symbols2 (preinstalled on linux Mint)
- Noto Color Emoji (preinstalled on linux Mint)

# Installation
There is an installer script which is able to install the needed dependencies and to symlink the dotfiles.

	./install

without any parameters it prints the usage.

The install script basically installs the dependencies on ubuntu/debian based systens and 
renames old dotfiles and symlinks to the ones from this package.
If you are not on a debian-based distro you need to install the deendencies yourself and invoke the installer with
	./install -d
to symlink the dotfiles only.
