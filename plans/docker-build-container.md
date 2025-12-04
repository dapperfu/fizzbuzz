# Docker Build Container for FizzBuzz

Create a Dockerfile that compiles all FizzBuzz implementations and validates them by running each binary, with Makefile integration for Docker operations.

## Implementation Details

### Dockerfile Structure
- **Base Image**: `ubuntu:24.04`
- **Compilers to Install**:
  - `gcc` and `g++` (via `build-essential` package)
  - `rustc` (via `rustc` package or rustup)
  - `go` (via `golang-go` package)
  - Python3 is included by default in Ubuntu 24.04, no additional installation needed
- **Source Files**: Copy all source files (`fizzbuzz.c`, `fizzbuzz.cpp`, `fizzbuzz.go`, `fizzbuzz.rs`, `fizzbuzz.py`) into the container
- **Compilation**: Compile each source file to produce binaries matching the Makefile targets:
  - `fizzbuzz_c` from `fizzbuzz.c`
  - `fizzbuzz_cpp` from `fizzbuzz.cpp`
  - `fizzbuzz_go` from `fizzbuzz.go`
  - `fizzbuzz_rs` from `fizzbuzz.rs`
- **Python**: Run `python3 fizzbuzz.py` directly (no compilation needed)
- **Validation**: Run each compiled binary and the Python script, then append output to `output_docker.txt` with headers indicating which implementation produced the output

### Files to Create/Modify
- `Dockerfile` - Main Docker build file in project root
- `Makefile` - Add Docker-related targets:
  - `docker-all` - Build Docker image, run container, and validate (main target)
  - `docker-build` - Build the Docker image
  - `docker-run` - Run the container and generate output_docker.txt
  - `docker-clean` - Remove Docker image and container artifacts
  - `docker-test` - Build image and run validation (alias for docker-all)

### Compilation Commands
Based on [Makefile](Makefile):
- C: `gcc -o fizzbuzz_c fizzbuzz.c`
- C++: `g++ -o fizzbuzz_cpp fizzbuzz.cpp`
- Go: `go build -o fizzbuzz_go fizzbuzz.go`
- Rust: `rustc -o fizzbuzz_rs fizzbuzz.rs`
- Python: `python3 fizzbuzz.py` (no compilation needed, run directly)

### Validation Output Format
The `output_docker.txt` file should contain:
- Section headers for each implementation (C, C++, Go, Rust, Python)
- Full output from running each binary/script
- Clear separation between implementations

### Makefile Integration
Add Docker targets to [Makefile](Makefile):
- `docker-all`: Build image, run container, display results (default Docker target)
- `docker-build`: Build the Docker image with appropriate tag (e.g., `fizzbuzz:build`)
- `docker-run`: Execute the container and generate output_docker.txt
- `docker-clean`: Remove Docker image, containers, and output_docker.txt
- `docker-test`: Alias for docker-all for consistency with other test targets

Docker image should be tagged appropriately (e.g., `fizzbuzz:build` or `fizzbuzz:latest`)

## Implementation Todos
1. Create Dockerfile with Ubuntu 24.04 base, install all required compilers (gcc, g++, rustc, go), copy all source files including Python, compile all binaries, and run validation script
2. Add validation step in Dockerfile that runs each compiled binary and Python script, appending output to output_docker.txt with proper headers
3. Add Docker-related targets to Makefile: docker-all, docker-build, docker-run, docker-clean, docker-test

