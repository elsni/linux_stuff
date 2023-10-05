# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

### Functions ###
exec_if_exists() {
	test -x $1 && $1
}

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
#[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
force_color_prompt=yes

PROMPT_ALTERNATIVE=twoline
NEWLINE_BEFORE_PROMPT=yes


if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

# Fancy prompt taken from Kali Linux bashrc

if [ "$color_prompt" = yes ]; then
    # override default virtualenv indicator in prompt
	VIRTUAL_ENV_DISABLE_PROMPT=1

	prompt_color='\[\033[;32m\]'
    info_color='\[\033[1;34m\]'
    prompt_symbol=@
   	if [ "$EUID" -eq 0 ]; then # Change prompt colors for root user
       prompt_color='\[\033[;94m\]'
       info_color='\[\033[1;31m\]'
       prompt_symbol=@
   	fi
   	case "$PROMPT_ALTERNATIVE" in
        twoline)
            PS1=$prompt_color'┌──${debian_chroot:+($debian_chroot)──}${VIRTUAL_ENV:+(\[\033[0;1m\]$(basename $VIRTUAL_ENV)'$prompt_color')}('$info_color'\u${prompt_symbol}\h'$prompt_color')-[\[\033[0;1m\]\w'$prompt_color']\n'$prompt_color'└─'$info_color'\$\[\033[0m\] ';;
        oneline)
            PS1='${VIRTUAL_ENV:+($(basename $VIRTUAL_ENV)) }${debian_chroot:+($debian_chroot)}'$info_color'\u@\h\[\033[00m\]:'$prompt_color'\[\033[01m\]\w\[\033[00m\]\$ ';;
        backtrack)
            PS1='${VIRTUAL_ENV:+($(basename $VIRTUAL_ENV)) }${debian_chroot:+($debian_chroot)}\[\033[01;31m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ ';;
        block)
            PS1='\n \[\033[0;34m\]╭─────\[\033[0;31m\]\[\033[0;37m\]\[\033[41m\] \u \[\033[0m\]\[\033[0;31m\]\[\033[0;34m\]─────\[\033[0;32m\]\[\033[0;30m\]\[\033[42m\] \w \[\033[0m\]\[\033[0;32m\] \n \[\033[0;34m\]╰ \[\033[1;36m\]\$ \[\033[0m\] ';;
   	esac
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi


unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='exa'
    alias dir='dir --color=auto'
    alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'
export EXA_COLORS="da=6;37;40"
export GTK_THEME=Adapta-Nokto:dark
export SUDO_ASKPASS=/usr/bin/ssh-askpass

# some more ls aliases
alias ll='eza -al'
alias la='eza -a'
alias l='eza -aF'

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

export PATH="$HOME/bin:$HOME/.local/bin:/opt/gcc-eabi/bin:/usr/games:$PATH"

PATH="/home/elsni/perl5/bin${PATH:+:${PATH}}"; export PATH;
PERL5LIB="/home/elsni/perl5/lib/perl5${PERL5LIB:+:${PERL5LIB}}"; export PERL5LIB;
PERL_LOCAL_LIB_ROOT="/home/elsni/perl5${PERL_LOCAL_LIB_ROOT:+:${PERL_LOCAL_LIB_ROOT}}"; export PERL_LOCAL_LIB_ROOT;
PERL_MB_OPT="--install_base \"/home/elsni/perl5\""; export PERL_MB_OPT;
PERL_MM_OPT="INSTALL_BASE=/home/elsni/perl5"; export PERL_MM_OPT;

# -------------------------------------------------------------------------------
# some more useful stuff
# -------------------------------------------------------------------------------

# 'cd' to the most recently modified directory in $PWD
cl() {
    last_dir="$(ls -Frt | grep '/$' | tail -n1)"
    if [ -d "$last_dir" ]; then
    cd "$last_dir"
    fi
}

# Move 'up' so many directories instead of using several cd ../../, etc.
up() { cd $(eval printf '../'%.0s {1..$1}) && pwd; }

#Another variation of the one above
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias .....="cd ../../../.."

# since ifconfig is deprecated we need a substitute
alias ifconfig="ip -c a"

# for showing all mqtt messages
alias mqtt="mosquitto_sub -v -h localhost -p 1883 -t '#'"


# Do X stuff only when we have an X display
if xhost >& /dev/null; then
  # deactivate capsloack key
  xmodmap -e "keycode 66 ="
fi

# make SDL stop complaining about no mouse
export SDL_NOMOUSE="1"

# -------------------------------------------------------------------------------
# Message to show on login
# -------------------------------------------------------------------------------
echo
neofetch
echo "Welcome to"
hostname | figlet | lolcat
echo

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

export GOROOT="/usr/local/go"
export GOPATH=$HOME/source/go
export PATH=$GOPATH/bin:$GOROOT/bin:$PATH:~/zig

# show local machine info if exists
exec_if_exists ~/.machineinfo

# Red block nonblinking cursor
echo -e '\033[?112;0;64c'
