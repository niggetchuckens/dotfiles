export PATH="~/.local/bin:$PATH"

if [ -n "$VIRTUAL_ENV" ]; then
    source "$VIRTUAL_ENV/bin/activate"
fi

if [ -x /usr/bin/dircolors ]; then
  test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
  alias ls='ls --color=auto'
  alias grep='grep --color=auto'
  alias fgrep='fgrep --color=auto'
  alias egrep='egrep --color=auto'
fi

alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias z='clear'
alias tempswap='.scripts/temp-swap.sh'
alias cleancache='.scripts/cleancache.sh'

clear
fastfetch
eval "$(oh-my-posh init bash --config ~/.config/oh-my-posh/bubblesextra.omp.json)"

