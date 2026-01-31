@echo off
REM Regression Test Runner
REM 1. Compiles the code (requires g++ in PATH)
REM 2. Runs the dipole simulation
REM 3. Compares output against golden data

echo [1/3] Compiling PFFDTD...
g++ -std=c++11 -O3 src/pffdtd.cpp -o pffdtd.exe
if %ERRORLEVEL% NEQ 0 (
    echo Compilation failed! Make sure g++ is in your PATH.
    exit /b 1
)

echo [2/3] Running Simulation...
if not exist tests\regression\output mkdir tests\regression\output

REM Run with dipole input
REM Usage: pffdtd <input_file> <output_prefix>
pffdtd.exe dipole.str tests\regression\output\dipole_test

if %ERRORLEVEL% NEQ 0 (
    echo Simulation failed!
    exit /b 1
)

echo [3/3] Comparing Results...
python tests/regression/compare_results.py --golden_dir tests/regression/golden --new_dir tests/regression/output

if %ERRORLEVEL% NEQ 0 (
    echo TESTS FAILED
    exit /b 1
) else (
    echo ALL TESTS PASSED
)
