# Use the official Debian bookworm image as the base image
FROM debian:bookworm

# Use bash for the following commands
SHELL ["/bin/bash", "-c"]

# Add application code to the image
ADD . /XOR_based_DNA_encoding

# Set the working directory for subsequent instructions
WORKDIR /XOR_based_DNA_encoding

# Install necessary system packages and clean up
RUN apt-get update && apt-get full-upgrade -y \
    && apt-get install -y git python3-full python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Create a Python virtual environment
RUN python3 -m venv xorenv

# Activate the virtual environment and install Python dependencies
RUN source xorenv/bin/activate && \
    python3 -m pip install numpy && \
    python3 -m pip install .

# Set environment variable to ensure virtual environment is activated
ENV PATH="/XOR_based_DNA_encoding/xorenv/bin:${PATH}"
