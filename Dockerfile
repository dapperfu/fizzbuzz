# Dockerfile for FizzBuzz Build and Validation
# Base image: Ubuntu 24.04
FROM ubuntu:24.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install all required compilers and build tools
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    gcc \
    g++ \
    rustc \
    golang-go \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all source files
COPY fizzbuzz.c fizzbuzz.cpp fizzbuzz.go fizzbuzz.rs fizzbuzz.py /app/

# Compile all binaries
RUN gcc -o fizzbuzz_c fizzbuzz.c && \
    g++ -o fizzbuzz_cpp fizzbuzz.cpp && \
    go build -o fizzbuzz_go fizzbuzz.go && \
    rustc -o fizzbuzz_rs fizzbuzz.rs

# Validate by running all implementations and capturing output
RUN echo "=== C Implementation ===" > output_docker.txt && \
    ./fizzbuzz_c >> output_docker.txt && \
    echo "" >> output_docker.txt && \
    echo "=== C++ Implementation ===" >> output_docker.txt && \
    ./fizzbuzz_cpp >> output_docker.txt && \
    echo "" >> output_docker.txt && \
    echo "=== Go Implementation ===" >> output_docker.txt && \
    ./fizzbuzz_go >> output_docker.txt && \
    echo "" >> output_docker.txt && \
    echo "=== Rust Implementation ===" >> output_docker.txt && \
    ./fizzbuzz_rs >> output_docker.txt && \
    echo "" >> output_docker.txt && \
    echo "=== Python Implementation ===" >> output_docker.txt && \
    python3 fizzbuzz.py >> output_docker.txt

# Default command: display the validation output
CMD ["cat", "output_docker.txt"]

