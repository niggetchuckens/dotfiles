export PATH="~/.local/bin:$PATH"

# Auto-detect and activate Python virtual environments
auto_venv() {
    local venv_path=""
    # Check for virtual environments in the current directory
    for dir in .venv venv .env env; do
        if [[ -f "$PWD/$dir/bin/activate" ]]; then
            venv_path="$PWD/$dir"
            break
        fi
    done

    if [[ -n "$venv_path" ]]; then
        # Activate if it's not already active
        if [[ "$VIRTUAL_ENV" != "$venv_path" ]]; then
            if declare -f deactivate >/dev/null; then
                deactivate
            fi
            source "$venv_path/bin/activate"
        fi
    else
        # If no venv in the current directory, check if we need to deactivate
        if [[ -n "$VIRTUAL_ENV" ]]; then
            local parent_dir=$(dirname "$VIRTUAL_ENV")
            # Deactivate if we left the project directory
            if [[ "$PWD" != "$parent_dir"* ]]; then
                if declare -f deactivate >/dev/null; then
                    deactivate
                fi
            fi
        fi
    fi
}

cd() { builtin cd "$@" && auto_venv; }
pushd() { builtin pushd "$@" > /dev/null && auto_venv; }
popd() { builtin popd "$@" > /dev/null && auto_venv; }

# Run once on initialization
auto_venv

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
alias tempswap='~/.scripts/temp-swap.sh'
alias cleancache='~/.scripts/cleancache.sh'

clear
fastfetch
eval "$(oh-my-posh init bash --config ~/.config/oh-my-posh/bubblesextra.omp.json)"


# Added by Antigravity CLI installer
export PATH="/home/hime/.local/bin:$PATH"

# Global AutoTor Aliases
alias tor-run='sudo python3 ~/.scripts/GlobalAutoTor.py start'
alias tor-kill='sudo python3 ~/.scripts/GlobalAutoTor.py stop'
