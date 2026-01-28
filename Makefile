# Makefile for PF-FDTD Project
# 
# Usage:
#   make              - Build optimized version
#   make debug        - Build debug version
#   make clean        - Remove compiled binaries
#   make test         - Run tests (when available)
#   make parallel     - Build with OpenMP (future)
#
# Compiler settings
CXX = g++
CXXFLAGS_BASE = -std=c++11 -Wall -Wextra
CXXFLAGS_DEBUG = $(CXXFLAGS_BASE) -O0 -g -DDEBUG
CXXFLAGS_RELEASE = $(CXXFLAGS_BASE) -O3 -march=native -DNDEBUG

# Directories
SRC_DIR = src
BIN_DIR = .
TEST_DIR = tests

# Source files
SOURCES = $(SRC_DIR)/pffdtd.cpp
HEADERS = $(SRC_DIR)/plasma.h $(SRC_DIR)/output.h $(SRC_DIR)/source.h \
          $(SRC_DIR)/Retard.h $(SRC_DIR)/memallocate.h

# Output
TARGET = $(BIN_DIR)/pffdtd
TARGET_DEBUG = $(BIN_DIR)/pffdtd_debug

# Default target
.PHONY: all
all: release

# Release build (optimized)
.PHONY: release
release: CXXFLAGS = $(CXXFLAGS_RELEASE)
release: $(TARGET)

# Debug build
.PHONY: debug
debug: CXXFLAGS = $(CXXFLAGS_DEBUG)
debug: $(TARGET_DEBUG)

# Compile main executable
$(TARGET): $(SOURCES) $(HEADERS)
	@echo "Building optimized release version..."
	$(CXX) $(CXXFLAGS) -o $@ $(SOURCES)
	@echo "Build complete: $@"

$(TARGET_DEBUG): $(SOURCES) $(HEADERS)
	@echo "Building debug version..."
	$(CXX) $(CXXFLAGS) -o $@ $(SOURCES)
	@echo "Build complete: $@"

# Clean build artifacts
.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	rm -f $(TARGET) $(TARGET_DEBUG)
	rm -f *.o *.a
	rm -f gmon.out
	@echo "Clean complete"

# Run basic test (when test suite is available)
.PHONY: test
test: $(TARGET)
	@echo "Running basic test (dipole antenna)..."
	@if [ -f "$(TEST_DIR)/data/dipole.str" ]; then \
		./$(TARGET) $(TEST_DIR)/data/dipole.str $(TEST_DIR)/output/dipole; \
		echo "Test complete - check $(TEST_DIR)/output/dipole.vc and .fd"; \
	else \
		echo "Test input file not found at $(TEST_DIR)/data/dipole.str"; \
	fi

# Profile with gprof
.PHONY: profile
profile: CXXFLAGS = $(CXXFLAGS_BASE) -O2 -g -pg
profile: $(TARGET)
	@echo "Compiled for profiling with gprof"

# Help
.PHONY: help
help:
	@echo "PF-FDTD Makefile Targets:"
	@echo ""
	@echo "  make release     - Build optimized release version (default)"
	@echo "  make debug       - Build debug version with symbols"
	@echo "  make test        - Run basic test case"
	@echo "  make profile     - Build for profiling with gprof"
	@echo "  make clean       - Remove compiled binaries"
	@echo "  make help        - Show this help message"
	@echo ""
	@echo "Environment Variables:"
	@echo "  CXX              - C++ compiler (default: g++)"
	@echo "  CXXFLAGS         - C++ compiler flags"
	@echo ""
	@echo "Examples:"
	@echo "  make                    # Build optimized version"
	@echo "  make debug              # Build debug version"
	@echo "  make test               # Run test case"
	@echo "  CXX=clang++ make        # Build with Clang"

# Phony targets
.PHONY: install uninstall

# Future targets (not implemented yet)
install:
	@echo "Install target not yet implemented"

uninstall:
	@echo "Uninstall target not yet implemented"

# Parallel builds (future)
.PHONY: parallel
parallel:
	@echo "Parallel build not yet available"
	@echo "Planned for v2.0 with OpenMP support"

# GPU builds (future)
.PHONY: gpu
gpu:
	@echo "GPU build not yet available"
	@echo "Planned for v2.0 with CUDA support"

# Silence make warnings
SHELL := /bin/bash
.SILENT: help
