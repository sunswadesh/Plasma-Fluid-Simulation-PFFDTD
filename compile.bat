@echo off
REM Build OpenMP PF-FDTD. Default output is versioned so older binaries are kept.
REM   compile.bat              -> pffdtd_parallel_rs_t.exe  (Paper 2 kinematic rs(t))
REM   compile.bat baseline     -> pffdtd_parallel.exe       (static-sheath / campaign name)

setlocal
echo Compiling PFFDTD Parallel Version (OpenMP)...

where g++ >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: g++ compiler not found in PATH.
    echo Please install MinGW-w64 or add it to your PATH.
    exit /b 1
)

set OUT=pffdtd_parallel_rs_t.exe
if /I "%~1"=="baseline" set OUT=pffdtd_parallel.exe
if /I "%~1"=="rs_t" set OUT=pffdtd_parallel_rs_t.exe

echo Output: %OUT%

g++ -std=c++11 -O3 -fopenmp src/pffdtd.cpp src/utils/memallocate.cpp src/io/file_handler.cpp src/io/output.cpp src/source/source.cpp src/fields/field_calculator.cpp src/physics/plasma.cpp -o %OUT%

if %ERRORLEVEL% EQU 0 (
    echo Compilation Successful!
    echo Created %OUT%
) else (
    echo Compilation Failed!
    exit /b 1
)

endlocal
