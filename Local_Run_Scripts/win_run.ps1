# Check if Docker is installed
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Output "Docker is not installed. Please install Docker and try again."
    exit 1
}

# Build the Docker image
docker build -t nse_analyser .

# Check if a container named 'nse_analyser' exists
if (docker ps -aq -f name=nse_analyser) {
    # If it does, stop it
    docker stop nse_analyser
    # Then remove it
    docker container rm nse_analyser
}

# Run the Docker container
docker run --name nse_analyser -it -p 8080:8080 nse_analyser
