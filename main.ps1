$apps = @(
    'JanDeDobbeleer.OhMyPosh',
    'Fastfetch-cli.Fastfetch',
    'arndawg.tmux-windows',
    'Git.Git',
    'BurntSushi.ripgrep.MSVC',
    'GnuWin32.Grep',
    'aristocratos.btop4win'
)

foreach ($app in $apps) {
    Write-Output "Installing: $app"
    winget install --id $app --accept-source-agreements --accept-package-agreements
}

# Deploy .config directory to ~/.config
$targetConfig = Join-Path $HOME ".config"
if (-not (Test-Path $targetConfig)) {
    New-Item -ItemType Directory -Path $targetConfig -Force
}
$sourceConfig = Join-Path $PSScriptRoot ".config"
if (Test-Path $sourceConfig) {
    Copy-Item -Path "$sourceConfig\*" -Destination $targetConfig -Recurse -Force
    Write-Output "Configuration files deployed to $targetConfig"
}

# Deploy PowerShell profile
$profileDir = Split-Path -Path $PROFILE -Parent
if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force
}

$sourceProfile = Join-Path $PSScriptRoot ".config\Microsoft.PowerShell_profile.ps1"
if (Test-Path $sourceProfile) {
    Copy-Item -Path $sourceProfile -Destination $PROFILE -Force
    Write-Output "PowerShell profile deployed to $PROFILE"
}

# Prompt to run DevDebloat script
$debloatScript = Join-Path $PSScriptRoot "debloat-dev.ps1"
if (Test-Path $debloatScript) {
    Write-Output "`nDevDebloat script detected at $debloatScript"
    Write-Output "To run debloating, execute: .\debloat-dev.ps1 (or .\debloat-dev.ps1 -All)"
}