# Alias section
Set-Alias z clear
if (Get-Command btop4win -ErrorAction SilentlyContinue) {
    Set-Alias btop btop4win -ErrorAction SilentlyContinue
}
if (Get-Command rg -ErrorAction SilentlyContinue) {
    Set-Alias grep rg -ErrorAction SilentlyContinue
}

# Custom functions
function nc_server {
    $cloudflared = "C:\Program Files (x86)\cloudflared\cloudflared.exe"

    if (-not (Test-Path $cloudflared)) {
        Write-Error "Cloudflared not found at $cloudflared"
        return
    }
    
    try {
        ssh -o ProxyCommand="$cloudflared access ssh --hostname ssh.niggetchuckens.online" hime@ssh.niggetchuckens.online
    }
    catch {
        Write-Error "SSH connection failed: $_"
    }
}

function homelab {
    try {
        ssh hime@192.168.1.24
    }
    catch {
        Write-Error "SSH connection failed: $_"
    }
}

# Clears terminal and launch oh-my-posh if installed
cls
if (Get-Command fastfetch -ErrorAction SilentlyContinue) {
    fastfetch
}
if (Get-Command oh-my-posh -ErrorAction SilentlyContinue) {
    oh-my-posh init pwsh --eval --config ~/.config/oh-my-posh/bubblesextra.omp.json | Invoke-Expression
}
