# linux_stuff

Personal Linux dotfiles, a macOS Bash environment, and installers for the tools
used by those configurations. The Linux setup includes an optional herbstluftwm
X11 desktop; the macOS setup is limited to command-line tools and shell settings.

The installers link configuration into your home directory and can install
packages. Review the platform section before running an installation mode:
existing configuration is replaced, with backups for regular files and directories.

## Contents

- [Choose an installer](#choose-an-installer)
- [Repository layout](#repository-layout)
- [Debian-based distributions](#debian-based-distributions)
- [Gentoo](#gentoo)
- [macOS](#macos)
- [Installed configuration and backups](#installed-configuration-and-backups)
- [Shell environment](#shell-environment)
- [Linux desktop configuration](#linux-desktop-configuration)
- [Troubleshooting](#troubleshooting)
- [Development and validation](#development-and-validation)

## Choose an installer

| Platform | Installer | Scope |
| --- | --- | --- |
| Debian, Ubuntu, Mint, and other apt-based distributions | `./install_debian` | Console tools, optional fonts and X11 desktop packages, Linux dotfiles |
| Gentoo | `./install_gentoo` | Console tools, optional X11 desktop packages, Linux dotfiles |
| macOS | `./install_mac` | Bash environment, console tools, micro and Midnight Commander settings |

The former `install` entry point is now named `install_debian`. There is no
compatibility wrapper under the old name.

Run the appropriate installer without arguments to print its usage. Each accepts
one mode per invocation; the available modes differ between platforms. There is
no dry-run mode. `-p` prints dependencies without installing anything.

Run installers as the user whose home directory should receive the configuration.
Linux package operations request privileges through `sudo` where needed; running
an entire Linux installer with `sudo` can target root's home instead. The macOS
installer explicitly rejects root execution.

Keep the checkout at a permanent location. Installed symlinks point to absolute
paths inside it, so moving or deleting the repository breaks those links.

## Repository layout

```text
linux_stuff/
├── install_debian             # apt-based Linux installer
├── install_gentoo             # Gentoo/Portage installer
├── install_mac                # macOS shell installer
├── home/
│   ├── .bashrc                # Linux Bash settings
│   ├── .Xdefaults
│   ├── .Xresources
│   └── .config/               # Linux desktop and shared console settings
├── mac/
│   └── .bashrc                # macOS-specific Bash settings
├── tools/
│   ├── install_helpers.sh     # Shared backup helper
│   ├── get_st.sh              # Separate manual st terminal build helper
│   └── visualbell.diff        # Patch used by the st helper
├── tests/                     # Non-destructive installer checks
└── REVIEW.md                  # Review findings, resolutions, and test limits
```

The `st` build helper is separate from the installers and is intended for Linux.
None of the main installation modes runs it.

## Debian-based distributions

### Requirements

Use a Linux system with Bash and the apt package manager. Package installation
requires working package repositories, network access, and `sudo` privileges.
The script expects GNU `readlink -f` for source path resolution.

Package availability depends on your distribution and release. The installer
requests the package names directly; it does not translate unavailable packages
or automatically add alternative sources for them, apart from the eza repository
setup described below.

### Modes

| Mode | Package operations | Configuration |
| --- | --- | --- |
| No argument | None; print usage | None |
| `-p` | None; print dependency overview | None |
| `-c` | Console dependencies, eza, lolcat | All Linux dotfiles |
| `-k` | Console dependencies, eza, lolcat, terminal fonts | All Linux dotfiles |
| `-g` | Desktop dependencies and fonts | All Linux dotfiles |
| `-a` | Console and desktop dependencies, eza, lolcat, fonts | All Linux dotfiles |
| `-d` | None | All Linux dotfiles |

`-c` and `-k` do not install herbstluftwm or Polybar packages. All Linux
configuration directories are still linked, including desktop configuration.
`-g` installs desktop dependencies only; use `-a` for a complete fresh setup with
the commands required by the Bash greeting and aliases.

```sh
./install_debian -p   # inspect the dependency overview
./install_debian -c   # console setup
./install_debian -k   # console setup plus fonts, without a window manager
./install_debian -a   # complete console and X11 desktop setup
```

Choose one installation command for the setup you want; these examples are
alternatives, not a sequence to execute in full.

### Package and download behavior

Console packages include build tools, Git, curl, unzip, CA certificates,
fastfetch, toilet, Midnight Commander, nano, micro, and nala.

The console modes (`-c`, `-k`, and `-a`) also:

- Install eza through its upstream apt repository at `https://deb.gierens.de`.
  The script manages `/etc/apt/keyrings/gierens.gpg` and
  `/etc/apt/sources.list.d/gierens.list` when setting up the key.
- Clone or update `https://github.com/jaseg/lolcat.git` under `~/source/lolcat`,
  then run `make` and `sudo make install`.

The font modes (`-k`, `-g`, and `-a`) download the Fira Code Nerd Fonts ZIP from
release `v3.4.0`, extract it into `~/.local/share/fonts`, and run `fc-cache -f`.
The download temporarily uses `Fira_Code.zip` in the current working directory.

Desktop dependencies include herbstluftwm, Polybar, xterm, xwallpaper, rofi,
lxappearance, Alacritty, ssh-askpass, Noto fonts, emoji fonts, and Font Awesome.
Use `./install_debian -p` for the dependency overview maintained by the script.

## Gentoo

### Requirements

Use Gentoo with Bash, configured Portage repositories, and a working `emerge`.
Non-root users need `sudo` for package and Portage configuration changes. Emerge
may build packages from source, so installation time depends on the system.

The script checks the operating system before processing any mode. This also
applies to usage output and `-p`; run those commands on Gentoo.

### Modes

| Mode | Package operations | Configuration |
| --- | --- | --- |
| No argument | None; print usage | None |
| `-p` | None; print console and GUI package atoms | None |
| `-c` | Console packages and amd64 keyword entries | All Linux dotfiles |
| `-g` | GUI packages; refresh font cache if available | All Linux dotfiles |
| `-a` | Console and GUI packages | All Linux dotfiles |
| `-d` | None; no privilege escalation for linking | All Linux dotfiles |

```sh
./install_gentoo -p   # inspect package atoms
./install_gentoo -c   # console setup
./install_gentoo -a   # complete console and X11 desktop setup
```

Gentoo has no `-k` mode. As on Debian, `-g` does not install console dependencies,
and console-only installation still links the desktop configuration directories.

### Portage changes

The shell greeting uses `app-misc/fastfetch`. The console package list also
includes eza, micro, nano, Midnight Commander, toilet, lolcat, and build tools.
GUI packages include herbstluftwm, Polybar, Alacritty, rofi, and Fira Code.

For `-c` and `-a` on amd64, the script adds `~amd64` acceptance entries for
`app-editors/micro` and `games-misc/lolcat`. This is installer policy; the entries
are added regardless of whether a stable version would currently satisfy emerge.

If `/etc/portage/package.accept_keywords` is a directory, entries go into its
`elsni-env` file. If it is an existing regular file, entries are appended there.
Otherwise the directory and `elsni-env` file are created. Equivalent exact entries
are not appended again. Other architectures receive no automatic keyword entries.

Package operations use `emerge --ask=n`; the installer does not pause for
emerge's usual confirmation prompt.

## macOS

### Requirements and switching from zsh

Homebrew must already be installed. Bash must be the account's default login
shell; simply launching `bash` inside a zsh session is insufficient. The installer
checks the account setting with `dscl` and does not change it automatically.
Apple's Bash 3.2 is supported. To choose it yourself:

```sh
chsh -s /bin/bash
```

Then open a new terminal. To inspect the configured login shell:

```sh
dscl . -read "/Users/$(id -un)" UserShell
```

An executable Homebrew Bash can also be used as the default shell. The installer
does not install Bash or register additional shells.

### Finding Homebrew after a shell change

Settings from `.zshrc` are not automatically loaded by Bash. If Homebrew was
available only through your previous zsh configuration, `install_mac` can still
find it. The discovery order is:

1. A `brew` executable already available through `PATH`.
2. `$HOMEBREW_PREFIX/bin/brew`, if that variable is set and the file is executable.
3. The standard macOS locations: `/opt/homebrew/bin/brew` first on arm64, or
   `/usr/local/bin/brew` first on other architectures, followed by the other path.

For an existing custom installation outside PATH, supply its installation root:

```sh
HOMEBREW_PREFIX="/path/to/homebrew" ./install_mac -c
```

The installer initializes its environment with `brew shellenv` before package
operations. It also saves the detected executable's absolute path in the generated
`~/.bash_profile`, so later Bash login shells initialize the same installation.
It does not read or execute your zsh startup files or install Homebrew itself.

See the official [Homebrew installation and shell setup documentation](https://docs.brew.sh/Installation#post-installation-steps).

### Modes and first installation

| Mode | Package operations | Configuration |
| --- | --- | --- |
| No argument | None; print usage | None |
| `-p` | None; print Homebrew formula names | None |
| `-c` | Install console formulas through Homebrew | macOS shell and editor settings |
| `-d` | None; initialize existing Homebrew | macOS shell and editor settings |

```sh
./install_mac -p
./install_mac -c
```

After a successful installation, open a new terminal or load the generated profile
in your current Bash session:

```sh
source ~/.bash_profile
```

A child installer process cannot change the environment of the already-open parent
shell. Loading the profile or opening a new terminal makes the shell settings and
Homebrew PATH available there.

### Installed tools and configuration

The Homebrew formula list is:

```text
git curl unzip fastfetch toilet midnight-commander nano micro eza lolcat
```

The macOS installer links only these repository settings:

| Destination | Repository source |
| --- | --- |
| `~/.bashrc` | `mac/.bashrc` |
| `~/.config/micro` | `home/.config/micro` |
| `~/.config/mc` | `home/.config/mc` |

It also generates two regular files:

- `~/.bash_profile`: initializes the discovered Homebrew installation and sources
  `.bashrc` for interactive login shells.
- `~/.nanorc`: enables line numbers, cursor information, history, and syntax
  definitions from the detected Homebrew prefix's `share/nano` directory.

`-d` assumes dependencies are already installed and checks that Homebrew's nano
syntax directory exists. It is not a way to install a usable environment without
Homebrew. It does not individually validate every other console dependency.

Existing profile content is backed up rather than merged. If your previous Bash
profile contained other setup, review its backup and reapply the parts you need.

The macOS installer does not install X11, herbstluftwm, Polybar, rofi, Alacritty,
fonts, or Linux package managers. It does not link `.Xresources`, `.Xdefaults`,
or Linux desktop configuration. Native macOS `ifconfig` remains available.

## Installed configuration and backups

### Linux link destinations

Both Linux installers link `home/.bashrc`, `home/.Xresources`, and
`home/.Xdefaults` into the corresponding paths in `$HOME`. They also link each
immediate configuration directory under `home/.config` into `~/.config`:

```text
alacritty  herbstluftwm  mc  micro  nano  neofetch  polybar  rofi
```

The neofetch configuration is retained in the repository, although the shell
now runs fastfetch. Linux installers do not create or update `.bash_profile`.
They use `$HOME/.config` directly rather than an alternative `XDG_CONFIG_HOME`.

### Backup format

Before replacing an existing regular file or directory, the installer reserves a
unique directory alongside it and moves the old item into its `original` entry:

```text
~/.bashrc_old_20261028_143000.A1b2C3d4/original
~/.config/micro_old_20261028_143000.E5f6G7h8/original
```

The random suffix keeps backups separate even when timestamps are identical.
Existing symlinks, including broken ones, are removed and replaced directly;
the symlink itself is not backed up, and its target is not deleted.

Backups are not pruned automatically. Re-running Linux installation normally
replaces existing links without making another backup. Re-running macOS setup
also backs up its generated `.bash_profile` and `.nanorc` regular files.

Installation is not transactional. A later failure can leave earlier package or
configuration changes in place. Backups cover replaced home-directory files and
directories; they do not roll back package installations or system configuration.

### Restoring an item

Inspect the available backup directories and choose the one you want to restore.
For example, if `~/.bashrc` is still the installed symlink, restore it with:

```sh
unlink "$HOME/.bashrc"
mv "$HOME/.bashrc_old_20261028_143000.A1b2C3d4/original" "$HOME/.bashrc"
```

Replace the example backup path with an actual path on your system. `unlink`
removes the symlink, leaving the repository source intact. For a generated
regular file such as the macOS `.bash_profile`, move the current file aside
before moving the chosen backup's `original` entry back to its destination.

There is no automated uninstall command. Restore each required item separately;
removing packages, external apt sources, or Portage keyword entries is a separate
manual operation.

## Shell environment

Linux uses `home/.bashrc`; macOS uses `mac/.bashrc`. Both provide a two-line
coloured prompt, Bash history settings, eza listing aliases, directory shortcuts,
and a greeting using fastfetch, toilet, and lolcat. Optional local Node.js setup
under `~/.nvm` and an executable `~/.machineinfo` greeting script are loaded when
present. The installers do not install Node.js, NVM, or Go.

| Command | Purpose |
| --- | --- |
| `ls` | eza listing with icons, sorted by size, directories first |
| `ll` | Detailed listing with hidden entries and Git information |
| `ld` | List directories |
| `lf` | Detailed listing with file-type indicators |
| `lh` | List hidden entries |
| `lt` | Detailed listing sorted by modification time |
| `..`, `...`, `....`, `.....` | Move up one to four directory levels |
| `cl` | Enter the most recently modified immediate subdirectory |
| `up N` | Move up N directory levels |

Aliases override command names only in shells that load the configuration. Use
`command ls` to bypass the `ls` alias when you need the system implementation.
The macOS configuration aliases `nano` to `micro`; `command nano` invokes nano
itself. The Linux configuration currently leaves the `nano` command unchanged.

The macOS variant avoids Linux-specific paths, GTK variables, and X11 commands.
It sets `GOPATH` to `~/source/go`; the Linux variant additionally contains
machine-specific Go, Perl, AppImage, and toolchain path settings. Review those
Linux settings before adopting the configuration on another machine.

## Linux desktop configuration

### herbstluftwm

Edit `home/.config/herbstluftwm/autostart` to choose applications and layout:

| Variable | Default | Purpose |
| --- | --- | --- |
| `WIN` | `Mod4` | Main keyboard and mouse modifier |
| `ALT` | `Mod1` | Additional application-launch modifier |
| `SMALLSCREEN` | `false` | Select compact or large Polybar configuration |
| `TERMINAL` | `alacritty` | Preferred terminal |
| `BROWSER` | `brave-browser` | Browser |
| `FILEMANAGER` | `nemo` | File manager |
| `MUSICPLAYER` | `spotify` | Music player |
| `IDE` | `code` | Editor/IDE |
| `SETTINGSDIALOG` | `lxappearance` | Appearance settings |

The application choices are personal defaults. Brave, Nemo, Spotify, VS Code,
`nm-applet`, and `blueman-applet` are not installed by these scripts. Install
those separately or change the commands. The desktop configuration includes an
xterm option and a Firefox ESR browser option when those programs are available.

The monitor setup assumes connectors named `eDP-1` and `HDMI-1`; inspect and
adapt the xrandr commands for your hardware before starting this desktop.

| Shortcut | Action |
| --- | --- |
| `Super+Return` | Open terminal |
| `Super+Space` | Open rofi application launcher |
| `Super+Alt+B` | Open browser |
| `Super+Alt+N` | Open file manager |
| `Super+Alt+S` | Open music player |
| `Super+Alt+C` | Open IDE |
| `Super+Alt+L` | Open appearance settings |
| `Super+Escape` | Close focused window |
| `Super+,` / `Super+.` | Cycle workspaces |
| `Super+Arrow` | Move focus |
| `Super+Shift+Arrow` | Move window |
| `Super+Shift+R` | Reload herbstluftwm configuration |
| `Super+Shift+Q` | Quit herbstluftwm |

Here `Super` means the configured `WIN` modifier. The configuration also defines
workspace selection, splitting, resizing, floating mode, and mouse bindings.
Installing packages does not start a session or configure a display manager.

### Polybar and terminal appearance

Polybar includes workspace indicators, date/time, CPU and memory information,
temperature, audio, network status, and power controls. The configuration files
also contain a weather module configured for Lübeck, Germany; enabled modules
depend on the selected bar configuration.

Workspace scripts resolve their path through `${env:HOME}`. Hardware-specific
network and temperature settings, power commands, and the weather location may
need adjustment. Power actions also depend on the system's sudo/askpass setup.

`SMALLSCREEN` selects `config_small` or `config_large`. The autostart script copies
the selected file over `~/.config/polybar/config`; because that directory is
symlinked, this updates the repository's working copy. Edit the selected source
configuration when you want changes to survive the next desktop startup.

Alacritty configuration files are under `home/.config/alacritty`. They define a
dark theme and Fira Code font settings. Select an installed font with the required
symbols if icons appear as missing glyphs. The macOS installer leaves terminal
application and font configuration to the user.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `brew` worked in zsh but is missing in Bash | Run `./install_mac -c`; standard Homebrew installations are discovered without PATH setup. Then open a new terminal or source `.bash_profile`. |
| Homebrew is installed in a custom location | Supply its absolute installation root through `HOMEBREW_PREFIX` if brew is not in PATH. |
| macOS installer rejects the login shell | Check `dscl` output, select Bash with `chsh`, and open a new terminal. Starting a Bash subprocess alone does not change the account setting. |
| macOS configuration-only mode reports missing nano syntax | Install the Homebrew console dependencies with `./install_mac -c`, or install Homebrew nano before using `-d`. |
| Greeting reports a missing command | Install console dependencies. Linux `-g` and all `-d` modes assume relevant console tools already exist. |
| apt or emerge cannot resolve a package | Check the requested name/atom against the repositories enabled on your system; the installer stops rather than substituting another tool. |
| Shell settings did not change after installation | Start a new interactive Bash. On macOS, source `.bash_profile`; on Linux, check that your shell startup loads `.bashrc`. |
| Symlinks broke after moving the checkout | Run the appropriate installer with `-d` from the new location, with its platform prerequisites satisfied. |
| Desktop application shortcut does nothing | Check the configured application command and install it separately or change the setting. |
| Icons, monitor layout, or network modules look wrong | Check fonts, connector names, and hardware-specific Polybar settings. |

## Development and validation

Run the non-destructive tests with Python 3:

```sh
python3 -m unittest discover -s tests -v
```

The suite currently contains 18 tests covering shell syntax, isolated dotfile
installation and repeat runs, backup collisions, dependency declarations,
mocked installer dispatch, macOS prerequisite checks, Homebrew discovery and
architecture preference, interactive Bash startup, and directory navigation.

Tests use temporary homes and mocked Homebrew/platform commands. They do not
install real packages, change your account's login shell, or start an X11 session.
Apple's Bash 3.2 was used to verify the macOS shell configuration on the development
host. Successful tests do not prove package availability on every distribution
release or live behavior on every desktop.

See [REVIEW.md](REVIEW.md) for review findings and validation limits. Source changes
should include English function documentation, appropriate tests, and README
updates when behavior changes. Keep source files below 500 lines and commit each
work session with a meaningful message.
