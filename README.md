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
- very basic, work in progress

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
- Fira Code Font - you can use the included script ./installfonts

# Installation

	./installfonts

Installs the free and fantastic Fira Code font, to use with alacritty
terminal emulator.

	./install

The install script installs some dependencies for you
and symlinks the dotfiles

you need to be able to 'sudo'


