@echo off
echo Compiling PFFDTD Parallel Version (Optimized)...

REM Add MinGW to PATH (Adjust if needed)
set PATH=%PATH%;C:\mingw64\mingw64\bin

REM Check g++
g++ --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: g++ not working. Please check your MinGW installation.
    pause
    exit /b 1
)

REM Compile
echo Running g++...
g++ -std=c++11 -O3 -fopenmp src/pffdtd.cpp src/utils/memallocate.cpp src/io/file_handler.cpp src/io/output.cpp src/source/source.cpp src/fields/field_calculator.cpp src/physics/plasma.cpp -o pffdtd_parallel.exe

if %ERRORLEVEL% EQU 0 (
    echo Compilation Successful!
    echo Created pffdtd_parallel.exe
) else (
    echo Compilation Failed!
)
pause
