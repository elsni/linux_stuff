#!/usr/bin/env bash
# Shared helpers for the dotfile installers.

# Move an existing destination into a uniquely reserved backup directory.
backup_existing() {
  local dest="$1"
  local backup_dir
  backup_dir="$(mktemp -d "${dest}_old_$(date +%Y%m%d_%H%M%S).XXXXXXXX")"
  mv -- "$dest" "${backup_dir}/original"
}
