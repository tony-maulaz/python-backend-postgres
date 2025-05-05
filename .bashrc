if [ -f /etc/bashrc ]; then
      . /etc/bashrc   # --> Read /etc/bashrc, if present.
fi

export HISTSIZE=100000000
export HISTFILESIZE=100000000
export HISTCONTROL=erasedups
shopt -s histappend

export DISPLAY=:0.0

Black='\e[0;30m'        # Black
Red='\e[0;31m'          # Red
Green='\e[0;32m'        # Green
Yellow='\e[0;33m'       # Yellow
Blue='\e[0;34m'         # Blue
Purple='\e[0;35m'       # Purple
Cyan='\e[0;36m'         # Cyan
White='\e[0;37m'        # White

BBlack='\e[1;30m'       # Black
BRed='\e[1;31m'         # Red
BGreen='\e[1;32m'       # Green
BYellow='\e[1;33m'      # Yellow
BBlue='\e[1;34m'        # Blue
BPurple='\e[1;35m'      # Purple
BCyan='\e[1;36m'        # Cyan
BWhite='\e[1;37m'       # White

On_Black='\e[40m'       # Black
On_Red='\e[41m'         # Red
On_Green='\e[42m'       # Green
On_Yellow='\e[43m'      # Yellow
On_Blue='\e[44m'        # Blue
On_Purple='\e[45m'      # Purple
On_Cyan='\e[46m'        # Cyan
On_White='\e[47m'       # White

alias ls='ls -h --color'
alias ll="ls -lv --group-directories-first"
alias la='ll -A'

alias grep='grep --color'

alias ..="cd .."
alias ...="cd ../.."

alias g='git'
alias c='clear'

# Test connection type:
if [ -n "${SSH_CONNECTION}" ]; then
    CNX=${Green}        # Connected on remote machine, via ssh (good).
elif [[ "${DISPLAY%%:0*}" != "" ]]; then
    CNX=${ALERT}        # Connected on remote machine, not via ssh (bad).
else
    CNX=${BCyan}        # Connected on local machine.
fi


LS_COLORS='di=1;34:fi=92:ln=31:pi=96:so=96:bd=96:cd=96:or=31:mi=96:ex=33:*.rpm=90'
export LS_COLORS

export PS1="\[\e[33m\]\n\u@\[$CNX\]\h \[\e[32m\]\W \[\e[m\]\\n\$ "