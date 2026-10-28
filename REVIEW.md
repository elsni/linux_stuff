# Project review — 2026-10-28

## Findings

1. **High: backup names can collide and lose existing data.** Both installers use
   second-resolution timestamps followed by `mv` without collision protection
   (`install:45-47`, `install_gentoo:115-117`). When a regular-file backup already
   exists under the generated name, it is overwritten. Reproduced with the Gentoo
   helper in a temporary home using a fixed date: the first backup was replaced
   by the second file. Existing directory backups can instead absorb the next
   directory, making restoration ambiguous.
2. **Medium: Gentoo installs the wrong greeting dependency.**
   `install_gentoo:20` installs neofetch, but `home/.bashrc:204` executes fastfetch.
   On a fresh installation the greeting reports a missing command.
3. **Medium: terminal mode omits commands required by the installed shell.**
   `install:227-236` does not call `install_eza` or `install_lolcat`, unlike console
   mode. The installed `.bashrc` uses eza for ls and other aliases (lines 131-141)
   and lolcat for the greeting (line 205).
4. **Medium: workspace module uses a user-specific absolute path.**
   The Polybar configurations invoke `/home/elsni/.config/polybar/info-hlwm-workspaces.sh`.
   Installation under another username leaves the workspace module unable to
   execute its script (`home/.config/polybar/config_large:97`; also config_small
   and config).
5. **Medium: mouse bindings reference an undefined modifier.**
   `home/.config/herbstluftwm/autostart:179-181` uses `$Mod`, while the configured
   modifier is `$WIN` (line 6). The commands therefore receive `-Button1` etc.,
   rather than the configured modifier plus button.
6. **Low: dotfile installation unnecessarily invokes sudo.**
   `install_gentoo:110` runs `run_root true` for every link. Non-root users can
   receive password prompts even for `-d`; failures are silently ignored.

## Validation and scope

- Added three checks: syntax of maintained Bash scripts, apt dotfile installation
  and repeat installation in a temporary home, and dependency-list output.
- Run: `python3 -m unittest discover -s tests -v` — all three pass.
- Passing tests cover the listed basic behaviors; they do not establish that the
  findings above are fixed.
- No package installation, privileged command, or desktop startup was performed.
- Gentoo/apt package availability and live X11 behavior were not validated.
- ShellCheck was unavailable on this host.
- Existing conventions also violate the requested function-comment policy;
  the bundled micro filemanager Lua file has 1,366 lines, above the 500-line limit.
- Production scripts and configuration were left unchanged for this review.
