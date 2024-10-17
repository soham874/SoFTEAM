# Clear the console
Clear-Host

# Default values
$DEBUG_MODE = $false
$WORKER_COUNT = 8

# Parse arguments
param (
    [string]$DEBUG_MODE
)

if ($DEBUG_MODE -eq "") {
    $DEBUG_MODE = $false
}

# Check if Docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker is not installed. Please install Docker and try again."
    exit 1
}

# Define the network name
$NETWORK_NAME = "softeam-network"

# Check if the Docker network exists
$network = docker network ls | Where-Object { $_ -like "*$NETWORK_NAME*" }
if (-not $network) {
    Write-Host "Creating network: $NETWORK_NAME"
    docker network create $NETWORK_NAME
} else {
    Write-Host "Network $NETWORK_NAME already exists."
}

# Check if the redis-server container is running
$redisRunning = docker ps -q -f name=redis-server
if ($redisRunning) {
    Write-Host "Redis server is already running."
} else {
    Write-Host "Redis server is not running. Checking for existing containers..."
    
    # Check if any Redis container is stopped
    $redisStopped = docker ps -aq -f status=exited -f name=redis-server
    if ($redisStopped) {
        Write-Host "Starting existing redis-server container..."
        docker start redis-server
    } else {
        Write-Host "Pulling Redis image and starting a new container..."
        docker pull redis:latest
        
        # Start the redis-server container
        docker run -d --network $NETWORK_NAME --name redis-server -it -p 6379:6379 redis:latest
    }
}

# Check if Redis is running on port 6379
if (Test-NetConnection -ComputerName localhost -Port 6379).TcpTestSucceeded {
    Write-Host "Redis server is running on port 6379."
} else {
    Write-Host "Failed to start Redis server on port 6379."
}

# Adjust worker count in debug mode
if ($DEBUG_MODE -eq "true") {
    Write-Host "Starting application in debug mode with 1 worker"
    $WORKER_COUNT = 1
}

# Build the Docker image
docker build --build-arg WORKER_COUNT=$WORKER_COUNT -t softeam .

# Check if the container named 'softeam' exists
$softeamContainer = docker ps -aq -f name=softeam
if ($softeamContainer) {
    # Stop and remove existing container
    docker stop softeam
    docker container rm softeam
}

# Run the Docker container
docker run --network $NETWORK_NAME --name softeam -it -p 8080:8080 -p 5678:5678 `
    -e DEBUG_MODE=$DEBUG_MODE `
    softeam
