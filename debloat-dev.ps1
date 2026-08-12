<#
.SYNOPSIS
    DevDebloat - Windows AI, Ads & Telemetry Removal Script for Developers & Gamers.

.DESCRIPTION
    Strips Windows AI (Copilot, Recall, Cortana), ads, suggestions, and telemetry
    inspired by AtlasOS and KernelOS, but specifically crafted for Developers and Gamers.
    
    CRITICAL PRESERVATIONS:
    - WSL 2 & Hyper-V Virtualization
    - Docker Desktop & Container Services (HNS, HvHost)
    - Xbox Live / Game Pass authentication & Gaming Services
    - Anticheat compatibility (Core Isolation / Windows Defender intact)
    - Windows Store & WinGet
    - Windows Terminal & PowerShell environment

.PARAMETER All
    Applies all debloat and optimization modules.

.PARAMETER DisableAI
    Disables Recall, Copilot, Cortana, and Edge AI integrations via Registry and Policies.

.PARAMETER DisableAds
    Disables Start Menu ads/suggestions, Bing search in Start, Lock screen Spotlight ads, Explorer sync ads, and Widgets.

.PARAMETER DisableTelemetry
    Disables diagnostic data collection, telemetry services (DiagTrack, dmwappushservice), and tracking scheduled tasks.

.PARAMETER RemoveBloatware
    Removes pre-installed consumer AppX bloatware (Candy Crush, Solitaire, News, Weather, Movies & TV, etc.)
    while strictly preserving Terminal, WinGet, Store, WSL, and Gaming Services.

.PARAMETER OptimizeDevGaming
    Enables Win32 Long Paths (crucial for git/node_modules), Hardware-Accelerated GPU Scheduling (HAGS),
    Game Mode, and ensures WSL/Hyper-V/Docker services are correctly configured.

.PARAMETER CreateRestorePoint
    Creates a Windows System Restore Point prior to applying changes.

.PARAMETER Interactive
    Launches an interactive menu to choose which debloat modules to execute.

.PARAMETER WhatIf
    Simulates actions without making any system changes (Dry Run).

.EXAMPLE
    .\debloat-dev.ps1 -All
    Runs all debloating and developer/gaming optimizations.

.EXAMPLE
    .\debloat-dev.ps1 -DisableAI -DisableAds -WhatIf
    Previews AI and Ads disabling without modifying the system.

.EXAMPLE
    .\debloat-dev.ps1
    Launches the interactive GUI/CLI menu.
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param (
    [Switch]$All,
    [Switch]$DisableAI,
    [Switch]$DisableAds,
    [Switch]$DisableTelemetry,
    [Switch]$RemoveBloatware,
    [Switch]$OptimizeDevGaming,
    [Switch]$CreateRestorePoint,
    [Switch]$Interactive
)

# Set execution preferences
$ErrorActionPreference = 'SilentlyContinue'

# --- UI & Output Helpers ---
function Write-Header {
    param ([string]$Text)
    Write-Host "`n========================================================" -ForegroundColor Cyan
    Write-Host "  $Text" -ForegroundColor Cyan
    Write-Host "========================================================`n" -ForegroundColor Cyan
}

function Write-Step {
    param ([string]$Text)
    Write-Host "[*] " -NoNewline -ForegroundColor Yellow
    Write-Host $Text -ForegroundColor White
}

function Write-Success {
    param ([string]$Text)
    Write-Host "[+] " -NoNewline -ForegroundColor Green
    Write-Host $Text -ForegroundColor Gray
}

function Write-Warn {
    param ([string]$Text)
    Write-Host "[!] " -NoNewline -ForegroundColor Yellow
    Write-Host $Text -ForegroundColor Yellow
}

function Write-Info {
    param ([string]$Text)
    Write-Host "[i] " -NoNewline -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor Gray
}

# --- Elevation Check ---
function Test-IsAdmin {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

$isDryRun = $WhatIfPreference -or $PSCmdlet.MyInvocation.BoundParameters.ContainsKey('WhatIf')

if (-not (Test-IsAdmin)) {
    if ($isDryRun) {
        Write-Warn "Running in -WhatIf (Dry Run) mode without Administrator elevation..."
    }
    else {
        Write-Warn "Elevating script permissions to Administrator..."
        $arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
        if ($All) { $arguments += " -All" }
        if ($DisableAI) { $arguments += " -DisableAI" }
        if ($DisableAds) { $arguments += " -DisableAds" }
        if ($DisableTelemetry) { $arguments += " -DisableTelemetry" }
        if ($RemoveBloatware) { $arguments += " -RemoveBloatware" }
        if ($OptimizeDevGaming) { $arguments += " -OptimizeDevGaming" }
        if ($CreateRestorePoint) { $arguments += " -CreateRestorePoint" }
        if ($isDryRun) { $arguments += " -WhatIf" }

        Start-Process powershell.exe -Verb RunAs -ArgumentList $arguments
        exit
    }
}

# --- Safe Helpers ---
function Set-RegistryKeyProperty {
    param (
        [string]$Path,
        [string]$Name,
        [object]$Value,
        [string]$PropertyType = "DWord"
    )

    if ($PSCmdlet.ShouldProcess("${Path}\${Name}", "Set Registry Value: $Value ($PropertyType)")) {
        try {
            if (-not (Test-Path $Path)) {
                New-Item -Path $Path -Force -ErrorAction Stop | Out-Null
            }
            Set-ItemProperty -Path $Path -Name $Name -Value $Value -Type $PropertyType -Force -ErrorAction Stop | Out-Null
            Write-Success "Registry set: $Path -> $Name = $Value"
        }
        catch {
            Write-Warn "Failed to set registry ${Path}\${Name} - Error: $_"
        }
    }
}

function Set-ServiceStatus {
    param (
        [string]$ServiceName,
        [string]$StartupType = "Disabled",
        [bool]$Stop = $true
    )

    $svc = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
    if ($svc) {
        if ($PSCmdlet.ShouldProcess($ServiceName, "Set StartupType: $StartupType and Stop")) {
            try {
                Set-Service -Name $ServiceName -StartupType $StartupType -ErrorAction SilentlyContinue
                if ($Stop -and $svc.Status -eq 'Running') {
                    Stop-Service -Name $ServiceName -Force -ErrorAction SilentlyContinue
                }
                Write-Success "Service '$ServiceName' set to $StartupType"
            }
            catch {
                Write-Warn "Could not modify service '$ServiceName' - Error: $_"
            }
        }
    } else {
        Write-Info "Service '$ServiceName' not present (Skipping)."
    }
}

function Disable-ScheduledTaskSafe {
    param (
        [string]$TaskPath,
        [string]$TaskName
    )

    $task = Get-ScheduledTask -TaskPath $TaskPath -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($task) {
        if ($PSCmdlet.ShouldProcess("${TaskPath}${TaskName}", "Disable Scheduled Task")) {
            try {
                Disable-ScheduledTask -TaskPath $TaskPath -TaskName $TaskName -ErrorAction Stop | Out-Null
                Write-Success "Disabled task: ${TaskPath}${TaskName}"
            }
            catch {
                Write-Warn "Failed to disable task ${TaskPath}${TaskName} - Error: $_"
            }
        }
    }
}

# --- Module 0: Create Restore Point ---
function Invoke-CreateRestorePoint {
    Write-Header "Creating System Restore Point"
    if ($PSCmdlet.ShouldProcess("SystemRestore", "Create Restore Point 'DevDebloat_PreOptimization'")) {
        try {
            Enable-ComputerRestore -Drive "$env:SystemDrive" -ErrorAction SilentlyContinue
            Checkpoint-Computer -Description "DevDebloat_PreOptimization" -RestorePointType "MODIFY_SETTINGS" -ErrorAction Stop
            Write-Success "System Restore Point created successfully!"
        }
        catch {
            Write-Warn "Could not create restore point - Error: $_ (Ensure System Restore is enabled)."
        }
    }
}

# --- Module 1: Disable Windows AI (Recall, Copilot, Cortana) ---
function Invoke-DisableAI {
    Write-Header "Module 1: Disabling Windows AI Features (Recall, Copilot, Cortana)"

    # Disable Windows Copilot
    Write-Step "Disabling Windows Copilot via Registry & Group Policy..."
    Set-RegistryKeyProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot" -Name "TurnOffWindowsCopilot" -Value 1
    Set-RegistryKeyProperty -Path "HKCU:\SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot" -Name "TurnOffWindowsCopilot" -Value 1
    Set-RegistryKeyProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "ShowCopilotButton" -Value 0

    # Disable Windows Recall & AI Data Analysis
    Write-Step "Disabling Windows Recall AI Data Analysis & Snapshot Recording..."
    Set-RegistryKeyProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsAI" -Name "DisableAIDataAnalysis" -Value 1
    Set-RegistryKeyProperty -Path "HKCU:\SOFTWARE\Policies\Microsoft\Windows\WindowsAI" -Name "DisableAIDataAnalysis" -Value 1
    Set-RegistryKeyProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsAI" -Name "TurnOffRecall" -Value 1

    # Disable DISM Recall Feature if present (Windows 11 24H2+)
    if (Get-Command Disable-WindowsOptionalFeature -ErrorAction SilentlyContinue) {
        $recallFeature = Get-WindowsOptionalFeature -Online -FeatureName "Recall" -ErrorAction SilentlyContinue
        if ($recallFeature -and $recallFeature.State -eq "Enabled") {
            if ($PSCmdlet.ShouldProcess("OptionalFeature: Recall", "Disable DISM Feature")) {
                Write-Step "Disabling DISM Windows Optional Feature: Recall..."
                Disable-WindowsOptionalFeature -Online -FeatureName "Recall" -NoRestart -ErrorAction SilentlyContinue | Out-Null
                Write-Success "Disabled Recall DISM Optional Feature."
            }
        }
    }

    # Disable Cortana & AI Sidebar in Edge
    Write-Step "Disabling Cortana and Edge Copilot Hubs..."
    Set-RegistryKeyProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Edge" -Name "HubsSidebarEnabled" -Value 0
    Set-RegistryKeyProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Edge" -Name "CopilotEnabled" -Value 0
    Set-RegistryKeyProperty -Path "HKCU:\SOFTWARE\Microsoft\Speech_OneCore\Preferences" -Name "VoiceActivationDefaultOff" -Value 1

    Write-Success "Windows AI features disabled."
}

# --- Module 2: Disable Ads, Suggestions & Widgets ---
function Invoke-DisableAds {
    Write-Header "Module 2: Disabling Windows Ads, Start Suggestions & Widgets"

    # Start Menu Suggestions & Bing Search
    Write-Step "Disabling Start Menu Ads & Bing Search in Start..."
    Set-RegistryKeyProperty -Path "HKCU:\SOFTWARE\Policies\Microsoft\Windows\Explorer" -Name "DisableSearchBoxSuggestions" -Value 1
    Set-RegistryKeyProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Search" -Name "BingSearchEnabled" -Value 0
    Set-RegistryKeyProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Search" -Name "CortanaConsent" -Value 0
    Set-RegistryKeyProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "Start_IrisRecommendations" -Value 0
    Set-RegistryKeyProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "Start_AccountNotifications" -Value 0

    # Content Delivery Manager (Consumer bloat auto-install)
    Write-Step "Disabling Consumer Experience background app installs & tips..."
    Set-RegistryKeyProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\CloudContent" -Name "DisableWindowsConsumerFeatures" -Value 1
    
    $cdmPath = "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager"
    Set-RegistryKeyProperty -Path $cdmPath -Name "SilentInstalledAppsEnabled" -Value 0
    Set-RegistryKeyProperty -Path $cdmPath -Name "SystemPaneSuggestionsEnabled" -Value 0
    Set-RegistryKeyProperty -Path $cdmPath -Name "SoftLandingEnabled" -Value 0
    Set-RegistryKeyProperty -Path $cdmPath -Name "SubscribedContent-338388Enabled" -Value 0 # Tips
    Set-RegistryKeyProperty -Path $cdmPath -Name "SubscribedContent-338389Enabled" -Value 0 # Get Started
    Set-RegistryKeyProperty -Path $cdmPath -Name "SubscribedContent-353694Enabled" -Value 0 # Suggested apps
    Set-RegistryKeyProperty -Path $cdmPath -Name "SubscribedContent-353696Enabled" -Value 0 # Settings ads
    Set-RegistryKeyProperty -Path $cdmPath -Name "SubscribedContent-310093Enabled" -Value 0 # Welcome experience
    Set-RegistryKeyProperty -Path $cdmPath -Name "SubscribedContent-338387Enabled" -Value 0 # Lockscreen ads

    # Lock Screen & File Explorer Ads
    Write-Step "Disabling Lock Screen Spotlight ads & Explorer sync ads..."
    Set-RegistryKeyProperty -Path $cdmPath -Name "RotatingLockScreenOverlayEnabled" -Value 0
    Set-RegistryKeyProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "ShowSyncProviderNotifications" -Value 0

    # Windows Widgets / News & Interests
    Write-Step "Disabling Windows Widgets & Taskbar News..."
    Set-RegistryKeyProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Dsh" -Name "AllowNewsAndInterests" -Value 0
    Set-RegistryKeyProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "TaskbarDa" -Value 0

    Write-Success "Windows Ads, Suggestions, and Widgets disabled."
}

# --- Module 3: Disable Telemetry & Tracking ---
function Invoke-DisableTelemetry {
    Write-Header "Module 3: Disabling Telemetry & Diagnostic Data Collection"

    Write-Step "Setting Telemetry Level to Basic/Security..."
    Set-RegistryKeyProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection" -Name "AllowTelemetry" -Value 0
    Set-RegistryKeyProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection" -Name "AllowTelemetry" -Value 0
    Set-RegistryKeyProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Privacy" -Name "TailoredExperiencesWithDiagnosticDataEnabled" -Value 0
    Set-RegistryKeyProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Feedback\Diagnostics" -Name "NumberOfSIUFInPeriod" -Value 0

    # Telemetry Services
    Write-Step "Disabling Telemetry Services (DiagTrack, dmwappushservice)..."
    Set-ServiceStatus -ServiceName "DiagTrack" -StartupType "Disabled" -Stop $true
    Set-ServiceStatus -ServiceName "dmwappushservice" -StartupType "Disabled" -Stop $true

    # Scheduled Tasks
    Write-Step "Disabling Customer Experience & Diagnostic Scheduled Tasks..."
    Disable-ScheduledTaskSafe -TaskPath "\Microsoft\Windows\Application Experience\" -TaskName "Microsoft Compatibility Appraiser"
    Disable-ScheduledTaskSafe -TaskPath "\Microsoft\Windows\Application Experience\" -TaskName "ProgramDataUpdater"
    Disable-ScheduledTaskSafe -TaskPath "\Microsoft\Windows\Customer Experience Improvement Program\" -TaskName "Consolidator"
    Disable-ScheduledTaskSafe -TaskPath "\Microsoft\Windows\Customer Experience Improvement Program\" -TaskName "KernelCeipTask"
    Disable-ScheduledTaskSafe -TaskPath "\Microsoft\Windows\Customer Experience Improvement Program\" -TaskName "UsbCeip"
    Disable-ScheduledTaskSafe -TaskPath "\Microsoft\Windows\DiskDiagnostic\" -TaskName "Microsoft-Windows-DiskDiagnosticDataCollector"
    Disable-ScheduledTaskSafe -TaskPath "\Microsoft\Windows\Feedback\Siuf\" -TaskName "DmClient"

    Write-Success "Telemetry and diagnostic tracking disabled."
}

# --- Module 4: Remove Pre-installed AppX Bloatware ---
function Invoke-RemoveBloatware {
    Write-Header "Module 4: Removing Consumer AppX Bloatware"

    # Explicit list of apps to KEEP (DO NOT REMOVE)
    $protectedApps = @(
        'Microsoft.WindowsTerminal',
        'Microsoft.PowerShell',
        'Microsoft.DesktopAppInstaller', # WinGet
        'Microsoft.WindowsStore',
        'Microsoft.StorePurchaseApp',
        'Microsoft.WSL',
        'Microsoft.GamingServices',
        'Microsoft.XboxIdentityProvider',
        'Microsoft.Xbox.TCUI',
        'Microsoft.XboxGameCallableUI',
        'Microsoft.XboxSpeechToTextOverlay',
        'Microsoft.DirectX',
        'Microsoft.VCLibs',
        'Microsoft.NET',
        'Microsoft.UI.Xaml',
        'Microsoft.SecHealthUI' # Windows Security UI
    )

    # Targeted Bloatware Apps
    $bloatwareApps = @(
        'Microsoft.5499814F5B107',        # Cortana
        'Microsoft.Copilot',             # Copilot App
        'Microsoft.BingNews',            # News
        'Microsoft.BingWeather',         # Weather
        'Microsoft.BingSearch',          # Bing Search
        'Microsoft.GetHelp',             # Get Help
        'Microsoft.Getstarted',          # Tips / Get Started
        'Microsoft.MicrosoftOfficeHub',  # Office Hub / 365
        'Microsoft.MicrosoftSolitaireCollection',
        'Microsoft.People',              # People App
        'Microsoft.PowerAutomateDesktop',
        'Microsoft.SkypeApp',            # Skype
        'Microsoft.Todos',               # To Do
        'Microsoft.WindowsFeedbackHub',  # Feedback Hub
        'Microsoft.WindowsMaps',         # Maps
        'Microsoft.YourPhone',           # Phone Link (remove consumer bloat)
        'Microsoft.ZuneVideo',           # Legacy Films & TV
        'Microsoft.ZuneMusic',           # Legacy Groove Music
        'Clipchamp.Clipchamp',           # Clipchamp
        '*Spotify*',
        '*TikTok*',
        '*Disney*',
        '*Facebook*',
        '*Netflix*'
    )

    Write-Step "Scanning and removing consumer bloatware packages..."

    foreach ($appPattern in $bloatwareApps) {
        # Check against protected list
        $isProtected = $false
        foreach ($protected in $protectedApps) {
            if ($appPattern -like "*$protected*" -or $protected -like "*$appPattern*") {
                $isProtected = $true
                break
            }
        }
        if ($isProtected) {
            Write-Info "Skipping protected app pattern: $appPattern"
            continue
        }

        # Current User AppX
        $oldWhatIf = $WhatIfPreference
        $WhatIfPreference = $false
        $userPackages = Get-AppxPackage -Name $appPattern -ErrorAction SilentlyContinue
        $provPackages = Get-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName -like $appPattern }
        $WhatIfPreference = $oldWhatIf

        foreach ($pkg in $userPackages) {
            if ($PSCmdlet.ShouldProcess($pkg.Name, "Remove User AppX Package")) {
                try {
                    Remove-AppxPackage -Package $pkg.PackageFullName -ErrorAction Stop
                    Write-Success "Removed User AppX: $($pkg.Name)"
                }
                catch {
                    Write-Warn "Could not remove $($pkg.Name) - Error: $_"
                }
            }
        }

        # Provisioned AppX (All Users future installs)
        foreach ($provPkg in $provPackages) {
            if ($PSCmdlet.ShouldProcess($provPkg.DisplayName, "Remove Provisioned AppX Package")) {
                try {
                    Remove-AppxProvisionedPackage -Online -PackageName $provPkg.PackageName -ErrorAction Stop | Out-Null
                    Write-Success "Removed Provisioned AppX: $($provPkg.DisplayName)"
                }
                catch {
                    Write-Warn "Could not remove provisioned $($provPkg.DisplayName) - Error: $_"
                }
            }
        }
    }

    Write-Success "Bloatware removal completed."
}

# --- Module 5: Developer & Gaming Optimizations ---
function Invoke-OptimizeDevGaming {
    Write-Header "Module 5: Developer & Gaming Optimizations"

    # 1. Enable Long Paths (Essential for Git & Node.js npm/yarn/pnpm deep nestings)
    Write-Step "Enabling Win32 Long Paths (filesystem limit removal)..."
    Set-RegistryKeyProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1

    # 2. Verify / Preserve Virtualization, WSL & Docker Services
    Write-Step "Ensuring WSL, Docker & Virtualization services are configured..."
    Set-ServiceStatus -ServiceName "LxssManager" -StartupType "Manual" -Stop $false
    Set-ServiceStatus -ServiceName "hns" -StartupType "Automatic" -Stop $false # Host Network Service for Docker/WSL2
    Set-ServiceStatus -ServiceName "vmms" -StartupType "Automatic" -Stop $false # Hyper-V Virtual Machine Management

    # 3. Gaming Optimizations: HAGS (Hardware-Accelerated GPU Scheduling) & Game Mode
    Write-Step "Enabling Hardware-Accelerated GPU Scheduling (HAGS) & Game Mode..."
    Set-RegistryKeyProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\GraphicsDrivers" -Name "HwSchMode" -Value 2
    Set-RegistryKeyProperty -Path "HKCU:\Software\Microsoft\GameBar" -Name "AllowAutoGameMode" -Value 1
    Set-RegistryKeyProperty -Path "HKCU:\Software\Microsoft\GameBar" -Name "AutoGameModeEnabled" -Value 1

    # 4. Preserve / Verify Gaming Services for Xbox & Game Pass
    Write-Step "Verifying Gaming Services and Xbox Authentication pipeline..."
    Set-ServiceStatus -ServiceName "GamingServices" -StartupType "Automatic" -Stop $false
    Set-ServiceStatus -ServiceName "GamingServicesNet" -StartupType "Automatic" -Stop $false
    Set-ServiceStatus -ServiceName "XblAuthManager" -StartupType "Manual" -Stop $false
    Set-ServiceStatus -ServiceName "XblGameSave" -StartupType "Manual" -Stop $false
    Set-ServiceStatus -ServiceName "XboxNetApiSvc" -StartupType "Manual" -Stop $false

    Write-Success "Developer & Gaming optimizations applied."
}

# --- Interactive Menu ---
function Show-InteractiveMenu {
    Clear-Host
    Write-Host "========================================================" -ForegroundColor Cyan
    Write-Host "  DevDebloat - Windows Debloater for Devs & Gamers" -ForegroundColor Cyan
    Write-Host "========================================================" -ForegroundColor Cyan
    Write-Host " Tailored for: WSL, Docker, Hyper-V, VS Code, Git & Gaming" -ForegroundColor Gray
    Write-Host ""
    Write-Host " Select options to execute:" -ForegroundColor White
    Write-Host "  [1] Run ALL Debloat & Optimization Modules (Recommended)" -ForegroundColor Green
    Write-Host "  [2] Disable Windows AI (Recall, Copilot, Cortana)" -ForegroundColor Yellow
    Write-Host "  [3] Disable Windows Ads, Start Suggestions & Widgets" -ForegroundColor Yellow
    Write-Host "  [4] Disable Telemetry & Diagnostic Data Tracking" -ForegroundColor Yellow
    Write-Host "  [5] Remove Consumer AppX Bloatware (Keep WSL/Gaming/Store)" -ForegroundColor Yellow
    Write-Host "  [6] Apply Developer & Gaming Optimizations (Long Paths, HAGS)" -ForegroundColor Yellow
    Write-Host "  [7] Create System Restore Point Only" -ForegroundColor Cyan
    Write-Host "  [Q] Quit" -ForegroundColor Red
    Write-Host ""

    $choice = Read-Host " Enter choice [1-7 or Q]"
    switch ($choice.ToUpper()) {
        "1" {
            Invoke-CreateRestorePoint
            Invoke-DisableAI
            Invoke-DisableAds
            Invoke-DisableTelemetry
            Invoke-RemoveBloatware
            Invoke-OptimizeDevGaming
        }
        "2" { Invoke-DisableAI }
        "3" { Invoke-DisableAds }
        "4" { Invoke-DisableTelemetry }
        "5" { Invoke-RemoveBloatware }
        "6" { Invoke-OptimizeDevGaming }
        "7" { Invoke-CreateRestorePoint }
        "Q" { Write-Host "Exiting without making changes." -ForegroundColor Gray; exit }
        default { Write-Warn "Invalid choice. Please run script again." }
    }
}

# --- Main Entry Point ---
if ($CreateRestorePoint) { Invoke-CreateRestorePoint }

if ($All) {
    if (-not $CreateRestorePoint) { Invoke-CreateRestorePoint }
    Invoke-DisableAI
    Invoke-DisableAds
    Invoke-DisableTelemetry
    Invoke-RemoveBloatware
    Invoke-OptimizeDevGaming
}
elseif ($DisableAI -or $DisableAds -or $DisableTelemetry -or $RemoveBloatware -or $OptimizeDevGaming) {
    if ($DisableAI) { Invoke-DisableAI }
    if ($DisableAds) { Invoke-DisableAds }
    if ($DisableTelemetry) { Invoke-DisableTelemetry }
    if ($RemoveBloatware) { Invoke-RemoveBloatware }
    if ($OptimizeDevGaming) { Invoke-OptimizeDevGaming }
}
else {
    Show-InteractiveMenu
}

Write-Header "Debloat Process Complete!"
Write-Host "Note: Some changes (such as Copilot/Recall registry policies & HAGS) require a restart to take full effect." -ForegroundColor Yellow
