#Requires -Version 7.3

<#
Run the release validation sequence.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

function Invoke-Step {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Section,

        [Parameter(Mandatory = $true)]
        [string]$Command,

        [Parameter(Mandatory = $true)]
        [scriptblock]$Script,

        [int[]]$AllowedExitCodes = @(0)
    )

    Write-Host ""
    Write-Host "============================================================"
    Write-Host $Section
    Write-Host "============================================================"
    Write-Host $Command

    $oldNativeErrorPreference = $PSNativeCommandUseErrorActionPreference

    try {
        # WHY: Capture and evaluate native exit codes ourselves so selected
        # advisory commands may report findings without stopping the release.
        $PSNativeCommandUseErrorActionPreference = $false

        & $Script
        $exitCode = $LASTEXITCODE
    }
    finally {
        $PSNativeCommandUseErrorActionPreference = $oldNativeErrorPreference
    }

    if ($exitCode -notin $AllowedExitCodes) {
        throw "$Section failed with exit code $exitCode."
    }

    if ($exitCode -ne 0) {
        Write-Host ""
        Write-Host "Command reported findings with allowed exit code $exitCode."
        Write-Host "Release validation will continue."
    }
}

# ============================================================
# === A) Toolchain refresh ===
# ============================================================

Invoke-Step "A1) Sync Python tooling" "uv lock --upgrade && uv sync --extra dev --extra docs" {
    uv lock --upgrade
    uv sync --extra dev --extra docs
}

Invoke-Step "A2) Install pre-commit hooks & update" "uvx pre-commit install && uvx pre-commit autoupdate" {
    uvx pre-commit install
    uvx pre-commit autoupdate
}

# ============================================================
# === C) Package command surface and manifest validation ===
# ============================================================

Invoke-Step "C1) Confirm public command is installed" "uv run se-theory-reference --help" {
    uv run se-theory-reference --help
}

Invoke-Step "C2) Confirm validate subcommand is exposed" "uv run se-theory-reference validate --help" {
    uv run se-theory-reference validate --help
}

Invoke-Step "C3) Confirm scaffold subcommand is exposed" "uv run se-theory-reference scaffold --help" {
    uv run se-theory-reference scaffold --help
}

Invoke-Step "C4) Confirm export subcommand is exposed" "uv run se-theory-reference export --help" {
    uv run se-theory-reference export --help
}

Invoke-Step "C5) Confirm catalog subcommand is exposed" "uv run se-theory-reference catalog --help" {
    uv run se-theory-reference catalog --help
}

Invoke-Step "C6) Confirm inspect subcommand is exposed" "uv run se-theory-reference inspect --help" {
    uv run se-theory-reference inspect --help
}

Invoke-Step "C7) Validate SE manifest against the published manifest schema" "uvx --from se-manifest-schema se-manifest validate-manifest --path SE_MANIFEST.toml --strict" {
    uvx --from se-manifest-schema se-manifest validate-manifest --path SE_MANIFEST.toml --strict
}

# ============================================================
# === D) Pre-commit and Python tests ===
# ============================================================

Invoke-Step "D1) Stage all changes so pre-commit sees tracked/staged files" "git add -A" {
    git add -A
}

Invoke-Step `
    "D2) Run pre-commit checks" `
    "uvx pre-commit run --all-files" `
    -AllowedExitCodes @(0, 1) {
    uvx pre-commit run --all-files
}

Invoke-Step "D3) Run pre-commit checks again after autofixes" "uvx pre-commit run --all-files" {
    uvx pre-commit run --all-files
}

Invoke-Step "D4) Run Python tests" "uv run python -m pytest" {
    uv run python -m pytest
}

Invoke-Step "D5) Run Pyright" "uv run python -m pyright" {
    uv run python -m pyright
}

Invoke-Step `
    "D6) Run pre-commit checks" `
    "uvx pre-commit run --all-files" `
    -AllowedExitCodes @(0, 1) {
    uvx pre-commit run --all-files
}

Invoke-Step "D7) Run final pre-commit check after tests/type checks" "uvx pre-commit run --all-files" {
    uvx pre-commit run --all-files
}

# ============================================================
# === E) Documentation ===
# ============================================================

Invoke-Step "E1) Build documentation" "uv run python -m zensical build" {
    uv run python -m zensical build
}

# ============================================================
# === F) Architectural and code-health checks ===
# ============================================================

Invoke-Step "F0) Check import layers" "`$env:PYTHONPATH = 'src'; uvx --python 3.13 --from import-linter lint-imports --config .github/.importlinter" {
    $oldPythonPath = $env:PYTHONPATH
    try {
        $env:PYTHONPATH = "src"
        uvx --python 3.13 --from import-linter lint-imports --config .github/.importlinter
    }
    finally {
        $env:PYTHONPATH = $oldPythonPath
    }
}

Invoke-Step `
    "F1) Find dead code" `
    "uvx --with-editable . vulture src/se_theory_reference_kit" `
    -AllowedExitCodes @(0, 3) {
    uvx --with-editable . vulture src/se_theory_reference_kit
}

Invoke-Step "F2) Check complexity; any output means C-or-worse complexity exists" "uvx radon cc src/se_theory_reference_kit -s -a -n C" {
    uvx radon cc src/se_theory_reference_kit -s -a -n C
}

Invoke-Step "F3) Report raw code metrics" "uvx radon raw src/se_theory_reference_kit -j | uv run python -c `"import json, sys; data=json.load(sys.stdin); keys=('loc','lloc','sloc','comments','multi','blank','single_comments'); totals={k:sum(file[k] for file in data.values()) for k in keys}; print('\n'.join(f'{k.upper()}: {v}' for k,v in totals.items()))`"" {
    uvx radon raw src/se_theory_reference_kit -j |
        uv run python -c "import json, sys; data=json.load(sys.stdin); keys=('loc','lloc','sloc','comments','multi','blank','single_comments'); totals={k:sum(file[k] for file in data.values()) for k in keys}; print('\n'.join(f'{k.upper()}: {v}' for k,v in totals.items()))"
}

# ============================================================
# === G) Distribution artifacts ===
# ============================================================

Invoke-Step "G1) Build source and wheel distributions" "uv build" {
    uv build
}

Invoke-Step "G2) Check distribution metadata" "uvx twine check dist/*" {
    uvx twine check dist/*
}

Write-Host ""
Write-Host "============================================================"
Write-Host "Release validation completed successfully."
Write-Host "============================================================"
