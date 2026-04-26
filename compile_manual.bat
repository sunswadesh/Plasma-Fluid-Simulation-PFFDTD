@echo off
echo Compiling PFFDTD Parallel Version (OpenMP)...

g++ -static -std=c++11 -O3 -fopenmp src/pffdtd.cpp src/utils/memallocate.cpp src/io/file_handler.cpp src/io/output.cpp src/source/source.cpp src/fields/field_calculator.cpp src/physics/plasma.cpp -o pffdtd_parallel.exe

if %ERRORLEVEL% EQU 0 (
    echo Compilation Successful!
    echo Created pffdtd_parallel.exe
) else (
    echo Compilation Failed!
    exit /b %ERRORLEVEL%
)
