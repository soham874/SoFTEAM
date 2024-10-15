# Check if Docker is installed
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Output "Docker is not installed. Please install Docker and try again."
    exit 1
}

# Build the Docker image
docker build -t softeam .

# Check if a container named 'softeam' exists
if (docker ps -aq -f name=softeam) {
    # If it does, stop it
    docker stop softeam
    # Then remove it
    docker container rm softeam
}

# Run the Docker container
docker run --name softeam -it -p 8080:8080 softeam
