#!/bin/bash
# Shared macOS account checks and Homebrew discovery.

# Report an error and stop before making further changes.
die() {
  echo "ERROR: $*" >&2
  exit 1
}

# Print standard Homebrew executables in the native architecture's order.
homebrew_locations() {
  case "$(uname -m)" in
    arm64) printf '%s\n' /opt/homebrew/bin/brew /usr/local/bin/brew ;;
    *) printf '%s\n' /usr/local/bin/brew /opt/homebrew/bin/brew ;;
  esac
}

# Locate existing Homebrew and initialize its environment for this installer.
initialize_homebrew() {
  BREW_COMMAND="$(command -v brew || true)"
  if [[ -z "$BREW_COMMAND" ]]; then
    local candidate
    if [[ -n "${HOMEBREW_PREFIX:-}" && -x "${HOMEBREW_PREFIX}/bin/brew" ]]; then
      BREW_COMMAND="${HOMEBREW_PREFIX}/bin/brew"
    else
      while IFS= read -r candidate; do
        if [[ -x "$candidate" ]]; then
          BREW_COMMAND="$candidate"
          break
        fi
      done < <(homebrew_locations)
    fi
  fi
  [[ -n "$BREW_COMMAND" ]] || die "Install Homebrew first; for a custom installation, set HOMEBREW_PREFIX."
  local shell_environment
  shell_environment="$("$BREW_COMMAND" shellenv)"
  eval "$shell_environment"
}

# Verify the operating system and account login shell, then initialize Homebrew.
require_mac_environment() {
  [[ "$(uname -s)" == Darwin ]] || die "This installer requires macOS."
  [[ "$EUID" -ne 0 ]] || die "Run this installer as your regular user, without sudo."
  local login_shell
  login_shell="$(dscl . -read "/Users/$(id -un)" UserShell)"
  login_shell="${login_shell#UserShell: }"
  [[ "${login_shell##*/}" == bash && -x "$login_shell" ]] ||
    die "Bash must be your default login shell. Set it with chsh before installation."
  initialize_homebrew
}

