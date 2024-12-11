# Define a script to automate container recreation with file copying
param (
    [string]$ContainerName # Accepts the name of the container as a parameter
)

# Define source and destination paths
$SourceFolder = "./Common-Utils"
$DestinationFolder = "./$ContainerName"

$commonUtilsPath = "$DestinationFolder\Common-Utils"
if (Test-Path -Path $commonUtilsPath) {
    Remove-Item -Recurse -Force -Path $commonUtilsPath
    Write-Host "Deleted Common-Utils from $DestinationFolder"
} else {
    Write-Host "Common-Utils does not exist in $DestinationFolder"
}

# Copy the contents of the source folder to the destination folder
try {
    Copy-Item -Path $SourceFolder -Destination $DestinationFolder -Recurse
    Write-Host "Successfully copied contents from '$SourceFolder' to '$DestinationFolder'."
} catch {
    Write-Host "Error copying files: $_" -ForegroundColor Red
    exit 1
}

# Run the Docker Compose command to recreate the container
$DockerCommand = "docker compose up -d --no-deps --build --force-recreate $ContainerName"
try {
    Write-Host "Executing: $DockerCommand"
    Invoke-Expression $DockerCommand
} catch {
    Write-Host "Error running Docker command: $_" -ForegroundColor Red
    exit 1
}

if (Test-Path -Path $commonUtilsPath) {
    Remove-Item -Recurse -Force -Path $commonUtilsPath
    Write-Host "Deleted Common-Utils from $DestinationFolder"
} else {
    Write-Host "Common-Utils does not exist in $DestinationFolder"
}

Write-Host "Container '$ContainerName' recreated successfully." -ForegroundColor Green
