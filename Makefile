# Makefile for PF-FDTD Project
# 
# Usage:
#   make              - Build optimized parallel version (default)
#   make serial       - Build optimized serial version
#   make debug        - Build debug version
#   make clean        - Remove compiled binaries
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
SOURCES = $(SRC_DIR)/pffdtd.cpp \
          $(SRC_DIR)/utils/memallocate.cpp \
          $(SRC_DIR)/io/file_handler.cpp \
          $(SRC_DIR)/io/output.cpp \
          $(SRC_DIR)/source/source.cpp \
          $(SRC_DIR)/fields/field_calculator.cpp \
          $(SRC_DIR)/physics/plasma.cpp

HEADERS = $(SRC_DIR)/physics/plasma.h $(SRC_DIR)/io/output.h $(SRC_DIR)/source/source.h \
          $(SRC_DIR)/utils/memallocate.h

# Output
TARGET_SERIAL = $(BIN_DIR)/pffdtd_serial
TARGET_PARALLEL = $(BIN_DIR)/pffdtd_parallel
TARGET_DEBUG = $(BIN_DIR)/pffdtd_debug

# Default target
.PHONY: all
all: parallel

# Parallel build (OpenMP) - Default
.PHONY: parallel
parallel: CXXFLAGS = $(CXXFLAGS_RELEASE) -fopenmp
parallel: $(TARGET_PARALLEL)

# Serial build
.PHONY: serial
serial: CXXFLAGS = $(CXXFLAGS_RELEASE)
serial: $(TARGET_SERIAL)

# Debug build
.PHONY: debug
debug: CXXFLAGS = $(CXXFLAGS_DEBUG)
debug: $(TARGET_DEBUG)

# Compile main executable (Parallel)
$(TARGET_PARALLEL): $(SOURCES) $(HEADERS)
	@echo "Building optimized parallel version..."
	$(CXX) $(CXXFLAGS) -o $@ $(SOURCES)
	@echo "Build complete: $@"

# Compile main executable (Serial)
$(TARGET_SERIAL): $(SOURCES) $(HEADERS)
	@echo "Building optimized serial version..."
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
	rm -f $(TARGET_SERIAL) $(TARGET_PARALLEL) $(TARGET_DEBUG)
	rm -f *.o *.a
	rm -f gmon.out
	@echo "Clean complete"

# Profile with gprof
.PHONY: profile
profile: CXXFLAGS = $(CXXFLAGS_BASE) -O2 -g -pg
profile: $(TARGET_SERIAL)
	@echo "Compiled for profiling with gprof"

# Help
.PHONY: help
help:
	@echo "PF-FDTD Makefile Targets:"
	@echo ""
	@echo "  make             - Build optimized parallel version (default)"
	@echo "  make serial      - Build optimized serial version"
	@echo "  make debug       - Build debug version with symbols"
	@echo "  make clean       - Remove compiled binaries"
	@echo "  make help        - Show this help message"
	@echo ""
	@echo "Environment Variables:"
	@echo "  CXX              - C++ compiler (default: g++)"
	@echo "  CXXFLAGS         - C++ compiler flags"
	@echo ""
