# Clear the screen
Clear-Host

# Default debug mode and worker count
$DEBUG_MODE = $false
$WORKER_COUNT = 8

Write-Host "Beginning setup of SoFTEAM project from scratch"

# Check if Docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker is not installed. Please install Docker and try again."
    exit 1
}

# Set environment variables
$env:DEBUG_MODE = $DEBUG_MODE
$env:WORKER_COUNT = $WORKER_COUNT

# List of directories to work with
$directories = @("Mission-Control", "Trading-Engine", "News-Gateway", "TechniSight", "Market-Gateway")

# Loop through each directory and delete Common-Utils
foreach ($dir in $directories) {
    $commonUtilsPath = "$dir\Common-Utils"
    if (Test-Path -Path $commonUtilsPath) {
        Remove-Item -Recurse -Force -Path $commonUtilsPath
        Write-Host "Deleted Common-Utils from $dir"
    } else {
        Write-Host "Common-Utils does not exist in $dir"
    }
}

# Loop through each directory and copy Common-Utils
foreach ($dir in $directories) {
    if (Test-Path -Path $dir) {
        if (Test-Path -Path "Common-Utils") {
            Copy-Item -Recurse -Path "Common-Utils" -Destination "$dir\Common-Utils"
            Write-Host "Copied Common-Utils into $dir"
        } else {
            Write-Host "Common-Utils directory does not exist"
        }
    } else {
        Write-Host "Directory $dir does not exist"
    }
}

# Root .env file path
$rootEnv = ".\.env"

# Remove the root .env file if it already exists
if (Test-Path -Path $rootEnv) {
    Remove-Item -Path $rootEnv
    Write-Host "Existing root .env file removed."
}

# Loop through each directory and append the content of its .env file to the root .env
foreach ($dir in $directories) {
    $envFile = "$dir\.env"
    if (Test-Path -Path $envFile) {
        Get-Content -Path $envFile | Add-Content -Path $rootEnv
        Write-Host "Appended $envFile to root .env"
    } else {
        Write-Host "$envFile does not exist, skipping..."
    }
}

Write-Host "All .env files merged into $rootEnv."

# Build and run containers
docker-compose up --build -d

# Remove the root .env file if it exists
if (Test-Path -Path $rootEnv) {
    Remove-Item -Path $rootEnv
    Write-Host "Existing root .env file removed."
}

Write-Host "Services created, copied env variables, and Common-Utils packages removed."

# Loop through each directory and delete Common-Utils again
foreach ($dir in $directories) {
    $commonUtilsPath = "$dir\Common-Utils"
    if (Test-Path -Path $commonUtilsPath) {
        Remove-Item -Recurse -Force -Path $commonUtilsPath
        Write-Host "Deleted Common-Utils from $dir"
    } else {
        Write-Host "Common-Utils does not exist in $dir"
    }
}

# Display docker stats
docker stats --all

Write-Host "Allowing grace period of 3 seconds before bringing down project..."
Start-Sleep -Seconds 3

# Stop and remove containers
docker-compose down
