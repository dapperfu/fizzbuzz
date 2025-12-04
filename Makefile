# Executables
C_EXE = fizzbuzz_c
CPP_EXE = fizzbuzz_cpp
RUST_EXE = fizzbuzz_rs
GO_EXE = fizzbuzz_go

# Source files
C_SRC = fizzbuzz.c
CPP_SRC = fizzbuzz.cpp
RUST_SRC = fizzbuzz.rs
GO_SRC = fizzbuzz.go
PYTHON_SRC = fizzbuzz.py

# C compilation
${C_EXE}: ${C_SRC}
	gcc -o ${C_EXE} ${C_SRC}

# C++ compilation
${CPP_EXE}: ${CPP_SRC}
	g++ -o ${CPP_EXE} ${CPP_SRC}

# Rust compilation
${RUST_EXE}: ${RUST_SRC}
	rustc -o ${RUST_EXE} ${RUST_SRC}

# Go compilation
${GO_EXE}: ${GO_SRC}
	go build -o ${GO_EXE} ${GO_SRC}

# Run targets
.PHONY: c
c: ${C_EXE}
	./${C_EXE}

.PHONY: cpp
cpp: ${CPP_EXE}
	./${CPP_EXE}

.PHONY: python
python: ${PYTHON_SRC}
	python3 ${PYTHON_SRC}

.PHONY: rust
rust: ${RUST_EXE}
	./${RUST_EXE}

.PHONY: go
go: ${GO_EXE}
	./${GO_EXE}

# All target - compile and run all implementations with headers
.PHONY: all
all:
	@echo "=== C Implementation ==="
	@${MAKE} c
	@echo ""
	@echo "=== C++ Implementation ==="
	@${MAKE} cpp
	@echo ""
	@echo "=== Python Implementation ==="
	@${MAKE} python
	@echo ""
	@echo "=== Rust Implementation ==="
	@${MAKE} rust
	@echo ""
	@echo "=== Go Implementation ==="
	@${MAKE} go

# Keep the original dev target
.PHONY: dev
dev:
	nano fizzbuzz.py && ./fizzbuzz.py > output.txt && cat output.txt && git add . && read -p "Press Enter to continue..." dummy && git commit -a

# Requirements documentation directories
DOORSTOP_HTML_DIR = docs/doorstop
STRICTDOC_HTML_DIR = docs/strictdoc/html

# Doorstop HTML generation
.PHONY: doorstop-html
doorstop-html:
	mkdir -p ${DOORSTOP_HTML_DIR}
	doorstop publish ${DOORSTOP_HTML_DIR}

# StrictDoc HTML generation
.PHONY: strictdoc-html
strictdoc-html:
	mkdir -p ${STRICTDOC_HTML_DIR}
	strictdoc export --formats html --output-dir ${STRICTDOC_HTML_DIR} docs/strictdoc

# Generate all requirements documentation
.PHONY: reqs-html
reqs-html: doorstop-html strictdoc-html
	@echo "Requirements documentation generated:"
	@echo "  Doorstop: ${DOORSTOP_HTML_DIR}"
	@echo "  StrictDoc: ${STRICTDOC_HTML_DIR}"

# Clean target
.PHONY: clean
clean:
	rm -f ${C_EXE} ${CPP_EXE} ${RUST_EXE} ${GO_EXE}
	rm -rf ${DOORSTOP_HTML_DIR} ${STRICTDOC_HTML_DIR}
