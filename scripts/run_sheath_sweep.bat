@echo off
setlocal EnableDelayedExpansion
pushd %~dp0..

REM Sheath Width Sweep: Sd = 0, 2, 4, 6, 8, 10 cells
REM Fixed params: fp=200kHz, fcol=0.1, fcyc=0, angles=0, T=2000K
REM Optional runtime args: VC step (arg 10), max iterations (arg 11)

if not exist "results\sheath_sweep" mkdir "results\sheath_sweep"
set "FAILED=0"
set "VC_STEP=10"
set "MAX_ITER=1000000"

echo ============================================
echo  Sheath Width Sweep (Sd = 0,2,4,6,8,10)
echo ============================================

for %%S in (0 2 4 6 8 10) do (
    echo.
    echo --- Running Sd=%%S ---
    set "OUTDIR=results\sheath_sweep\sd%%S"
    set "OUTBASE=!OUTDIR!\data"
    set "LOGFILE=!OUTDIR!\simulation.log"
    if not exist "!OUTDIR!" mkdir "!OUTDIR!"
    if exist "!OUTBASE!.vc" del /q "!OUTBASE!.vc"
    if exist "!OUTBASE!.fd" del /q "!OUTBASE!.fd"

    pffdtd_parallel.exe sheath "!OUTBASE!" 200000 0.1 0 0 0 2000 %%S !VC_STEP! !MAX_ITER! > "!LOGFILE!" 2>&1
    set "RC=!ERRORLEVEL!"

    if not "!RC!"=="0" (
        echo ERROR: Sd=%%S exited with code !RC!.
        set /a FAILED+=1
    ) else (
        if not exist "!OUTBASE!.vc" (
            echo ERROR: Sd=%%S produced no .vc output.
            set /a FAILED+=1
        ) else (
            for %%F in ("!OUTBASE!.vc") do set "VCSIZE=%%~zF"
            if "!VCSIZE!"=="0" (
                echo ERROR: Sd=%%S produced empty .vc output.
                set /a FAILED+=1
            ) else (
                echo OK: Sd=%%S completed. Output: !OUTBASE!.vc
            )
        )
    )
)

echo.
echo ============================================
echo  Sweep Complete. Results in results\sheath_sweep\
echo ============================================

set "EXITCODE=0"
if not "!FAILED!"=="0" set "EXITCODE=1"
if not "!FAILED!"=="0" echo Sweep finished with !FAILED! failure(s).

popd
endlocal & exit /b %EXITCODE%
