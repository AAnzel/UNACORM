# XOR based DNA encoding

## Usage in a Clean Environment (e.g., Docker)

### Building the Docker Image

To build the Docker image for the project, run the following command:

```bash
docker compose build
```

### Running the Docker Container

Start the container in detached mode using Docker Compose:

```bash
docker compose up -d
```

### Accessing the Container

To open a bash shell within the running container, use:

```bash
docker exec -it xor /bin/bash
```

This command allows you to interact with the container and run commands as needed.

### Running Python Scripts

Once inside the container, you can execute Python scripts with:

```bash
python3 python/examples/main.py
```

This command runs the specified Python script within the container's environment.
