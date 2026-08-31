# Shared paths for Tu (2008) sheath campaign scripts.
# Repo root = parent of projects/ (full PFFDtd tree). Override: $env:PFFDtd_ROOT

$script:ProjectRoot = Split-Path -Parent $PSScriptRoot
$script:RepoRoot = Split-Path -Parent $ProjectRoot
$script:PffdtdRoot = if ($env:PFFDtd_ROOT) { $env:PFFDtd_ROOT } else { $RepoRoot }
$script:InputsDir = Join-Path $ProjectRoot 'inputs'
$script:AnalysisDir = Join-Path $ProjectRoot 'analysis'

function Get-PffdtdExe {
    foreach ($exe in @(
        (Join-Path $PffdtdRoot 'pffdtd_parallel.exe'),
        (Join-Path $PffdtdRoot 'build\pffdtd_parallel.exe')
    )) {
        if (Test-Path $exe) { return $exe }
    }
    throw "pffdtd_parallel.exe not found under $PffdtdRoot (build with compile.bat or CMake)"
}

function Initialize-SheathRun {
    if (-not (Test-Path $PffdtdRoot)) {
        throw "PFFDtd repo root not found: $PffdtdRoot"
    }
    Get-ChildItem (Join-Path $InputsDir '*.str') -ErrorAction SilentlyContinue |
        Copy-Item -Destination $PffdtdRoot -Force
    Set-Location $PffdtdRoot
}
