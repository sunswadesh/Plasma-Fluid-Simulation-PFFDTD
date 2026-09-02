# Shared paths for Tu (2008) sheath campaign scripts.
# Repo root = collab repo (parent of projects/). Results and cwd always use RepoRoot.
# Optional: $env:PFFDtd_EXE_ROOT if the executable lives outside the repo.

$script:ProjectRoot = Split-Path -Parent $PSScriptRoot
# scripts -> tu2008-sheath -> projects -> collab repo root
$script:RepoRoot = (Resolve-Path (Join-Path $ProjectRoot '..\..')).Path
$script:PffdtdRoot = $RepoRoot
$script:InputsDir = Join-Path $ProjectRoot 'inputs'
$script:AnalysisDir = Join-Path $ProjectRoot 'analysis'

function Get-PffdtdExe {
    $searchRoots = @($RepoRoot)
    if ($env:PFFDtd_EXE_ROOT) {
        $searchRoots = @($env:PFFDtd_EXE_ROOT) + $searchRoots
    }
    foreach ($base in $searchRoots) {
        foreach ($exe in @(
            (Join-Path $base 'build\pffdtd_parallel.exe'),
            (Join-Path $base 'pffdtd_parallel.exe')
        )) {
            if (Test-Path $exe) { return $exe }
        }
    }
    throw "pffdtd_parallel.exe not found under $RepoRoot (run compile.bat or cmake --build build --target pffdtd_parallel)"
}

function Initialize-SheathRun {
    if (-not (Test-Path $PffdtdRoot)) {
        throw "Collab repo root not found: $PffdtdRoot"
    }
    Get-ChildItem (Join-Path $InputsDir '*.str') -ErrorAction SilentlyContinue |
        Copy-Item -Destination $PffdtdRoot -Force
    Set-Location $PffdtdRoot
}
