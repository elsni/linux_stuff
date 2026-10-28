# Interactive Bash settings for macOS; compatible with Apple's Bash 3.2.
case $- in
  *i*) ;;
  *) return ;;
esac

HISTCONTROL=ignoreboth
HISTSIZE=1000
HISTFILESIZE=2000
shopt -s histappend checkwinsize

# Use the same two-line prompt style as the Linux environment.
PS1='\[\033[;32m\]┌──(\[\033[1;34m\]\u@\h\[\033[;32m\])-[\w]\n└─\[\033[1;34m\]\$\[\033[0m\] '
export EXA_COLORS='da=6;37;40'

alias ld='eza -lDg --time-style long-iso'
alias lf='eza -lF --color=always --icons --time-style long-iso'
alias lh='eza -dl .* --group-directories-first --time-style long-iso'
alias ll='eza -alg --group-directories-first --icons --git --git-repos --time-style long-iso'
alias ls='eza -a --color=always --sort=size --group-directories-first --icons'
alias lt='eza -alg --sort=modified --git --git-repos --icons --time-style long-iso'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'
alias nano='micro'
alias sudo='sudo '

# Enter the most recently modified immediate subdirectory.
cl() {
  local last_dir
  last_dir="$(/bin/ls -tFd */ 2>/dev/null | head -n 1)"
  [[ -n "$last_dir" ]] && cd -- "$last_dir"
}

# Move up the requested positive number of directory levels.
up() {
  local levels="${1:-1}"
  local target='' index
  [[ "$levels" =~ ^[1-9][0-9]*$ ]] || { echo 'usage: up [positive integer]' >&2; return 1; }
  for ((index=0; index<levels; index++)); do
    target+='../'
  done
  cd -- "$target" && pwd
}

export PATH="$HOME/bin:$HOME/.local/bin:$PATH"
export GOPATH="$HOME/source/go"
export PATH="$GOPATH/bin:$PATH"

# Load optional local Node.js setup installed by the user.
export NVM_DIR="$HOME/.nvm"
[[ ! -s "$NVM_DIR/nvm.sh" ]] || source "$NVM_DIR/nvm.sh"
[[ ! -s "$NVM_DIR/bash_completion" ]] || source "$NVM_DIR/bash_completion"

fastfetch
printf 'Welcome to %s\n' "$(hostname)" | toilet -f future | lolcat

# Execute the optional machine-specific greeting script.
if [[ -x "$HOME/.machineinfo" ]]; then
  "$HOME/.machineinfo"
fi
