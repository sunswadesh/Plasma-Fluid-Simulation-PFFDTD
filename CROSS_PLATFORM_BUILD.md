# Cross-Platform Build Guide

## Overview

PF-FDTD is designed to run on both Windows and Linux systems. This guide covers the build process for both platforms using CMake, which provides a unified build system.

## Prerequisites

### Common Requirements
- CMake 3.10+ (download from https://cmake.org/)
- C++11 compatible compiler

### Windows Requirements
**Option 1: MinGW-w64 (Recommended)**
- Download from: https://www.mingw-w64.org/
- Choose: x86_64 architecture, POSIX threads, SEH exceptions
- Add to PATH: `C:\MinGW\bin`

**Option 2: Visual Studio Community**
- Download from: https://visualstudio.microsoft.com/
- Select "Desktop development with C++"
- CMake will auto-detect MSVC

**Option 3: Chocolatey (Easiest)**
```powershell
choco install mingw cmake
```

### Linux Requirements
Most Linux distributions come with GCC and CMake pre-installed. If not:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install build-essential cmake
```

**CentOS/RHEL/Fedora:**
```bash
sudo yum groupinstall "Development Tools"
sudo yum install cmake
```

**Arch Linux:**
```bash
sudo pacman -S base-devel cmake
```

## Build Instructions

### Step 1: Clone or Download
```bash
git clone https://github.com/sunswadesh/Plasma-Fluid-Simulation-PFFDTD.git
cd Plasma-Fluid-Simulation-PFFDTD
```

### Step 2: Configure Build
```bash
# Create build directory
mkdir build
cd build

# Configure with CMake
cmake ..
```

### Step 3: Build Targets

**Build all variants:**
```bash
cmake --build .
```

**Build specific target:**
```bash
# Debug version (recommended for testing)
cmake --build . --target pffdtd_debug

# Release version (production)
cmake --build . --target pffdtd_release

# Profile version (performance analysis)
cmake --build . --target pffdtd_profile

# Parallel version (if OpenMP available)
cmake --build . --target pffdtd_parallel
```

### Step 4: Run Tests

**Basic test with dipole antenna:**
```bash
# From build directory
cd bin/debug
./pffdtd_debug ../../dipole.str dipole_test
```

**Check output files:**
```bash
ls -la dipole_test.*
# Should see: dipole_test.vc dipole_test.fd
```

## Platform-Specific Notes

### Windows (MinGW)
```bash
# Build commands
cmake --build . --target pffdtd_debug

# Run executable
./pffdtd_debug.exe ../../dipole.str dipole_test
```

### Windows (Visual Studio)
```bash
# Use Visual Studio Developer Command Prompt
cmake --build . --config Debug --target pffdtd_debug

# Or open generated .sln file in Visual Studio
```

### Linux/macOS
```bash
# Build commands (same as Windows)
cmake --build . --target pffdtd_debug

# Run executable
./pffdtd_debug ../../dipole.str dipole_test
```

## Troubleshooting

### CMake Issues
**"CMake not found"**
- Windows: Add CMake to PATH or use full path
- Linux: `sudo apt install cmake` or `sudo yum install cmake`

**"Compiler not found"**
- Windows: Install MinGW-w64 and add to PATH
- Linux: `sudo apt install g++` or `sudo yum install gcc-c++`

### Build Errors
**OpenMP not found:**
- Windows: MinGW-w64 includes OpenMP
- Linux: `sudo apt install libomp-dev`

**Permission denied:**
- Windows: Run terminal as Administrator
- Linux: Use `sudo` for system-wide install

### Runtime Issues
**"Missing DLL" (Windows):**
- Install Microsoft Visual C++ Redistributables
- Or rebuild with static linking

**Segmentation fault:**
- Check input file format
- Verify memory allocation
- Use debug build for stack trace

## Advanced Configuration

### Custom Compiler
```bash
# Use specific compiler
export CC=/usr/bin/gcc-9
export CXX=/usr/bin/g++-9
cmake ..
```

### Build Optimization
```bash
# Release with specific architecture
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS="-march=haswell" ..
```

### Install System-Wide
```bash
# Install to /usr/local/bin (Linux/macOS)
sudo cmake --install .

# Install to custom location
cmake --install . --prefix /opt/pffdtd
```

## CI/CD Integration

### GitHub Actions (Linux/Windows/macOS)
```yaml
name: Build
on: [push, pull_request]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]

    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-cmake@v1
    - name: Build
      run: |
        mkdir build
        cd build
        cmake ..
        cmake --build . --target pffdtd_debug
```

## Performance Notes

- **Windows**: MSVC often faster than MinGW for release builds
- **Linux**: GCC with `-march=native` for best performance
- **macOS**: Clang with Xcode command line tools

## File Paths

The code uses relative paths and standard C file I/O, so it works identically on both platforms. No platform-specific path separators are used.

## Support

For build issues:
1. Check [DEVELOPMENT_SETUP.md](DEVELOPMENT_SETUP.md) for detailed setup
2. Verify CMake and compiler versions
3. Test with minimal example: `pffdtd dipole.str test_output`

---

**Last Updated:** January 28, 2026
**Tested On:** Windows 10 (MinGW), Ubuntu 20.04 (GCC), macOS 11 (Clang)