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
    param(
        [ValidateSet('auto','rs_t','baseline')]
        [string]$Variant = 'auto'
    )
    $names = switch ($Variant) {
        'rs_t'     { @('pffdtd_parallel_rs_t.exe', 'build\pffdtd_parallel_rs_t.exe') }
        'baseline' { @('pffdtd_parallel.exe', 'build\pffdtd_parallel.exe', 'build\bin\parallel\pffdtd_parallel.exe') }
        default    {
            @(
                'pffdtd_parallel_rs_t.exe',
                'build\pffdtd_parallel_rs_t.exe',
                'pffdtd_parallel.exe',
                'build\pffdtd_parallel.exe',
                'build\bin\parallel\pffdtd_parallel.exe'
            )
        }
    }
    $searchRoots = @($RepoRoot)
    if ($env:PFFDtd_EXE_ROOT) {
        $searchRoots = @($env:PFFDtd_EXE_ROOT) + $searchRoots
    }
    foreach ($base in $searchRoots) {
        foreach ($rel in $names) {
            $exe = Join-Path $base $rel
            if (Test-Path $exe) { return $exe }
        }
    }
    throw "pffdtd executable not found under $RepoRoot (run compile.bat or compile.bat baseline)"
}

function Initialize-SheathRun {
    if (-not (Test-Path $PffdtdRoot)) {
        throw "Collab repo root not found: $PffdtdRoot"
    }
    Get-ChildItem (Join-Path $InputsDir '*.str') -ErrorAction SilentlyContinue |
        Copy-Item -Destination $PffdtdRoot -Force
    Set-Location $PffdtdRoot
}
