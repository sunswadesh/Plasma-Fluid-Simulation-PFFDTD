# Development Environment Setup Guide

## Status: Missing Build Tools

Your Windows system is missing the necessary C++ development tools to compile the PFFDTD project.

## Required Tools

You need ONE of the following:

### Option 1: MinGW-w64 (Recommended for Unix Compatibility)
**Pros:** Same g++ compiler as Linux/Mac, works well with CMake
**Cons:** Separate installation

**Steps:**
1. Download from: https://www.mingw-w64.org/
2. Or use MinGW installer: https://osdn.net/projects/mingw/releases/
3. Choose: x86_64 architecture, POSIX thread model, SEH exception handling
4. Add to PATH: `C:\MinGW\bin`

**Install via Package Manager (Easier):**
```powershell
# Using Chocolatey (if installed)
choco install mingw

# Or using MSYS2
# Download from https://www.msys2.org/
# Then run: pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-make
```

### Option 2: Visual Studio Community Edition
**Pros:** Full IDE, native Windows compiler, many tools
**Cons:** Large download (~5 GB)

**Steps:**
1. Download from: https://visualstudio.microsoft.com/downloads/
2. Select "Desktop development with C++"
3. Install
4. Create Visual Studio project from existing code

**Quick Verification:**
```powershell
cl /?  # Should show MSVC compiler help
```

### Option 3: LLVM/Clang
**Pros:** Modern compiler, good C++ support
**Cons:** Less common on Windows

**Steps:**
1. Download from: https://releases.llvm.org/
2. Run installer with "Add LLVM to system PATH"
3. Use `clang++` instead of `g++`

## Install CMake (Recommended)

```powershell
# Using Chocolatey
choco install cmake

# Or download from: https://cmake.org/download/
# Then add to PATH
```

## Verify Installation

```powershell
# Check compiler
g++ --version          # MinGW
cl /?                  # Visual Studio
clang++ --version      # LLVM

# Check CMake
cmake --version
```

## For Your Project: Recommended Setup

**Best combination for PF-FDTD:**
1. **MinGW-w64** (compatible with existing Makefile)
2. **CMake** (cross-platform builds)
3. **Visual Studio Code** (lightweight editor)

This gives you the same tools as Linux/Mac users, making collaboration easier.

---

**Next Steps:**
1. Install MinGW-w64 and CMake
2. Add both to Windows PATH
3. Verify: `g++ --version` and `cmake --version`
4. Then we can test the build system

Would you like detailed installation steps for any of these options?
