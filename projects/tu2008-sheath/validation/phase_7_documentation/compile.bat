@echo off
setlocal
pushd %~dp0

where pdflatex >nul 2>&1
if errorlevel 1 (
  if exist "%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64" (
    set "PATH=%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64;%PATH%"
  )
)

where pdflatex >nul 2>&1
if errorlevel 1 (
  echo No TeX distribution found on PATH.
  echo Install MiKTeX or TeX Live, then re-run this script.
  echo Expected output: docs\progress_report\main.pdf
  popd
  exit /b 1
)

echo Using pdflatex
pdflatex -interaction=nonstopmode main.tex
if errorlevel 1 goto :fail
pdflatex -interaction=nonstopmode main.tex
if errorlevel 1 goto :fail

if exist main.pdf (
  echo Built main.pdf
  popd
  exit /b 0
)

:fail
echo Compile failed or main.pdf was not produced. Check main.log
popd
exit /b 1
