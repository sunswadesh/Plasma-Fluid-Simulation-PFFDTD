@echo off
pushd %~dp0..\..
echo Compiling Serial Version...
g++ -std=c++11 -O3 src/pffdtd.cpp src/utils/memallocate.cpp src/io/file_handler.cpp src/io/output.cpp src/source/source.cpp src/fields/field_calculator.cpp src/physics/plasma.cpp -o pffdtd_serial.exe
if %ERRORLEVEL% NEQ 0 (
    echo Compilation Failed. g++ not found or syntax error.
    popd
    exit /b 1
)

echo Running Benchmark...
mkdir tests\benchmarks\output 2>nul
echo Start Time: %TIME%
pffdtd_serial.exe dipole tests\benchmarks\output\bench_serial
echo End Time: %TIME%
popd
