# Download Absorption Libraries for Fraynix
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$goDir = Join-Path $scriptDir "go"
$cppDir = Join-Path $scriptDir "cpp"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  FRAYNIX ABSORPTION LIBRARY DOWNLOADER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    git --version | Out-Null
    Write-Host "Git found" -ForegroundColor Green
} catch {
    Write-Host "Git not found. Please install Git first." -ForegroundColor Red
    exit 1
}

# Function to clone a repository
function Clone-Repo {
    param([string]$Url, [string]$TargetDir, [string]$Name)
    
    if (Test-Path $TargetDir) {
        Write-Host "  $Name already exists, skipping..." -ForegroundColor Yellow
        return
    }
    
    Write-Host "  Downloading $Name..." -ForegroundColor Blue
    git clone --depth 1 $Url $TargetDir 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  $Name downloaded successfully" -ForegroundColor Green
    } else {
        Write-Host "  Failed to download $Name" -ForegroundColor Red
    }
}

# Go Libraries
Write-Host "GO LIBRARIES" -ForegroundColor Magenta
Write-Host "--------------------------------" -ForegroundColor Magenta
Clone-Repo "https://github.com/ollama/ollama.git" (Join-Path $goDir "ollama") "Ollama"
Clone-Repo "https://github.com/golang/go.git" (Join-Path $goDir "golang") "Golang"

# C++ Libraries
Write-Host ""
Write-Host "C++ LIBRARIES" -ForegroundColor Magenta
Write-Host "--------------------------------" -ForegroundColor Magenta
Clone-Repo "https://github.com/tensorflow/tensorflow.git" (Join-Path $cppDir "tensorflow") "TensorFlow"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DOWNLOAD COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Review downloaded libraries in absorption_libraries/" -ForegroundColor White
Write-Host "2. Use transpile command in Fraynix" -ForegroundColor White
Write-Host ""
