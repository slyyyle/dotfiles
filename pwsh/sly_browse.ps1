Clear-Host
Write-Host "=== Pane-Based Browser Launcher ===`n"

# Detect system capabilities
$wslInstalled = (Get-Command wsl -ErrorAction SilentlyContinue) -ne $null
$firefoxInstalled = (Get-Command firefox -ErrorAction SilentlyContinue) -ne $null
$edgeInstalled = (Get-Command msedge -ErrorAction SilentlyContinue) -ne $null

function Launch-WebView {
    if ($edgeInstalled) {
        Write-Host "`nLaunching Edge WebView..."
        Start-Process msedge -ArgumentList "--app=https://www.example.com" -NoNewWindow -Wait
    } else {
        Write-Host "`nEdge is not installed. Falling back to Firefox."
        Launch-Firefox
    }
}

function Launch-Firefox {
    if ($firefoxInstalled) {
        Write-Host "`nLaunching Firefox Kiosk Mode..."
        Start-Process firefox -ArgumentList "--kiosk https://www.example.com" -NoNewWindow -Wait
    } else {
        Write-Host "`nFirefox is not installed. Falling back to WSL browsers."
        Launch-TextBrowser
    }
}

function Launch-TextBrowser {
    if ($wslInstalled) {
        Write-Host "`nLaunching w3m (WSL) for text-based browsing..."
        wsl w3m https://www.example.com
    } else {
        Write-Host "`nWSL is not installed. Cannot use text-based browser."
    }
}

function Launch-Surf {
    if ($wslInstalled) {
        Write-Host "`nLaunching Surf (Minimal GUI Browser) via WSL..."
        wsl surf https://www.example.com
    } else {
        Write-Host "`nWSL is not installed. Cannot use Surf."
    }
}

# Display menu
Write-Host "Select a browsing mode:"
Write-Host "[1] Edge WebView (Recommended)"
Write-Host "[2] Firefox Kiosk Mode"
#Write-Host "[X] Text-Based Browser (w3m via WSL)"
#Write-Host "[X] Minimal GUI Browser (Surf via WSL)"
Write-Host "[3] Exit"

$choice = Read-Host "`nEnter your choice (1-5)"

switch ($choice) {
    "1" { Launch-WebView }
    "2" { Launch-Firefox }
#    "3" { Launch-TextBrowser }
#    "4" { Launch-Surf }
    "3" { Write-Host "`nExiting..."; exit }
    default { Write-Host "`nInvalid choice. Exiting..."; exit }
}
