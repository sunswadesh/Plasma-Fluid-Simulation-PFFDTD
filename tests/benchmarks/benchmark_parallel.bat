@echo off
pushd %~dp0..\..
echo Compiling Parallel Version (OpenMP)...
g++ -std=c++11 -O3 -fopenmp src/pffdtd.cpp src/utils/memallocate.cpp src/io/file_handler.cpp src/io/output.cpp src/source/source.cpp src/fields/field_calculator.cpp src/physics/plasma.cpp -o pffdtd_parallel.exe
if %ERRORLEVEL% NEQ 0 (
    echo Compilation Failed. g++ not found or syntax error.
    popd
    exit /b 1
)

echo Running Benchmark (Parallel)...
mkdir tests\benchmarks\output 2>nul
echo Start Time: %TIME%
pffdtd_parallel.exe dipole tests\benchmarks\output\bench_parallel
echo End Time: %TIME%
popd
