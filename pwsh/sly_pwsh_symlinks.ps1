# Define source and target paths
$target = $env:CURRENTUSER + "\.config\pwsh\sly_pwsh.ps1"
$symlink = $PROFILE.CurrentUserCurrentHost

# Ensure the target file exists before creating the symlink
if (!(Test-Path $target)) {
    Write-Host "Target file does not exist: $target" -ForegroundColor Red
    exit 1
}

# Remove existing symlink if it exists
if (Test-Path $symlink) {
    Remove-Item $symlink -Force
}

# Create the symlink
New-Item -ItemType SymbolicLink -Path $symlink -Target $target
Write-Host "Created symlink: $symlink -> $target" -ForegroundColor Green
