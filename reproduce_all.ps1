param(
    [string]$Root = (Resolve-Path $PSScriptRoot).Path,
    [switch]$SkipDownload,
    [switch]$SkipMaps,
    [switch]$SkipValidation
)
$ErrorActionPreference = 'Stop'
$env:INFLACION_ROOT = $Root

Write-Host '============================================================'
Write-Host ' Montevideo spatial prices / STM reproducibility pipeline'
Write-Host '============================================================'
Write-Host "Root: $Root"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Python is not available in PATH.' }

python -m pip install -r (Join-Path $PSScriptRoot 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }

$dirs = @('data_raw','data_intermediate','data_final','tables','figures','maps','logs')
foreach ($d in $dirs) { New-Item -ItemType Directory -Force -Path (Join-Path $Root $d) | Out-Null }

function Run-Python([string]$name) {
    $p = Join-Path $PSScriptRoot ('scripts\' + $name)
    Write-Host "`n>>> $name" -ForegroundColor Cyan
    python $p
    if ($LASTEXITCODE -ne 0) { throw "$name failed with exit code $LASTEXITCODE" }
}

if (-not $SkipDownload) {
    Write-Host "`n>>> 01_download_sipc_dimensions.ps1" -ForegroundColor Cyan
    & (Join-Path $PSScriptRoot 'scripts\01_download_sipc_dimensions.ps1')
    Run-Python '02_refresh_sipc_prices.py'
}

Run-Python '03_build_sipc_master.py'
Run-Python '04_build_spatial_price_index.py'
Run-Python '05_build_local_inflation.py'
Run-Python '06_robustify_neighborhood_inflation.py'
Run-Python '07_build_ccz_inflation.py'
Run-Python '09_build_ses_local_baskets.py'
Run-Python '10_build_relative_price_levels.py'
Run-Python '11_build_stm_route_geometry.py'
Run-Python '12_build_stm_ccz_network.py'

# Mapping is downstream-irrelevant. V5 has already downloaded the official CCZ ZIP;
# copy it to the location expected by the final mapping script.
if (-not $SkipMaps) {
    $srcCcz = Join-Path $Root 'data_raw\stm\ckan\sig_comunales.zip'
    $dstDir = Join-Path $Root 'data_raw\geography\ccz'
    $dstCcz = Join-Path $dstDir 'sig_comunales.zip'
    if (Test-Path $srcCcz) {
        New-Item -ItemType Directory -Force -Path $dstDir | Out-Null
        Copy-Item $srcCcz $dstCcz -Force
        Run-Python '08_make_ccz_maps.py'
    } else {
        Write-Warning 'Skipping CCZ maps: official CCZ ZIP was not found after STM stage.'
    }
}

Run-Python '13_build_mobility_market_panel.py'
Run-Python '14_build_spatial_market_access.py'
Run-Python '15_audit_spatial_access.py'
Run-Python '16_make_figures.py'

if (-not $SkipValidation) {
    Write-Host "`n>>> benchmark validation" -ForegroundColor Cyan
    python (Join-Path $PSScriptRoot 'verify_reproduction.py') --root $Root
    if ($LASTEXITCODE -ne 0) {
        throw 'Pipeline completed, but one or more benchmark outputs differ. See logs\reproduction_validation.csv.'
    }
}

Write-Host "`nREPRODUCTION PIPELINE COMPLETE" -ForegroundColor Green
