@echo off
setlocal
pushd %~dp0..

REM Parameters for Sheath Regime
REM freq_plasma (Hz) = 200e3 (approx for 5e8 density) -> 0.2 MHz
REM freq_collision = 0.1 (guess)
REM freq_cyclotron = 0 (B=0 for now?) or keep existing
REM angle_e = 0
REM angle_a = 0
REM T = 2000 (Kelvin)

REM pffdtd arguments:
REM 1: InputFile (dipole)
REM 2: OutputFile (results/sheath_test/data)
REM 3: FREQ_PLASMA (Hz? Input says MHz in prompts, checking pffdtd.cpp... "atof(argv[3])")
REM    In plasma.cpp: FREQ_PLASMA = 5.3e6 (default). In main: FREQ_PLASMA = atof(argv[3])
REM    Wait, if I pass 0.2, is it MHz or Hz?
REM    In plasma.cpp: "fp->%5.3f(MHz)" logic suggests it might store as Hz but print as MHz?
REM    Let's look at pffdtd.cpp line 269: printf("fp->%5.3f(MHz)", (FREQ_PLASMA/1e6));
REM    So FREQ_PLASMA is in Hz.
REM NOTA BENE: 30 kHz pump is the SOURCE frequency, not Plasma frequency.
REM Source freq is set in .str file (line 10: 100000000 = 100 MHz).
REM I need to update dipole.str or create sheath.str for 30 kHz source.

if not exist "results\sheath_test" mkdir "results\sheath_test"

REM Create sheath.str from dipole.str with 30 kHz source and no field output
powershell -Command "$c = Get-Content 'dipole.str'; for ($i = 0; $i -lt $c.Length; $i++) { if ($c[$i] -match '^//Output Field Info') { $c = $c[0..($i-1)]; break } }; $c = $c -replace '100000000','30000'; Set-Content 'sheath.str' $c"

echo Running Sheath Test...
REM Args: 
REM 1: sheath (input file base)
REM 2: results\sheath_test\data
REM 3: 200000 (F_plasma Hz = 200 kHz)
REM 4: 0.1 (F_col ratio)
REM 5: 0 (F_cyc Hz)
REM 6: 0 (Ang E)
REM 7: 0 (Ang A)
REM 8: 2000 (T Kelvin)

if exist "results\sheath_test\data.fd" del /q "results\sheath_test\data.fd"
pffdtd_parallel.exe sheath "results\sheath_test\data" 200000 0.1 0 0 0 2000 > "results\sheath_test\simulation.log" 2>&1

echo Done.
popd
