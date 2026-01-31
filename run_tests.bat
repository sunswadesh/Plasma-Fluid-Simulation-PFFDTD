@echo off
echo Running PFFDTD Tests...

if not exist build (
    mkdir build
)

cd build
cmake ..
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

cmake --build . --target unit_tests
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

ctest -C Debug --output-on-failure
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

echo All tests passed!
cd ..
