param(
    [string]$OutputDirectory = "release"
)

$ErrorActionPreference = "Stop"
$projectDirectory = $PSScriptRoot
$outputDirectoryPath = Join-Path $projectDirectory $OutputDirectory
$workDirectoryPath = Join-Path `
    ([IO.Path]::GetTempPath()) `
    ("Crea_Report_build_" + [Guid]::NewGuid().ToString("N"))
$executablePath = Join-Path $outputDirectoryPath "Crea_Report.exe"

Push-Location $projectDirectory
try {
    python -m PyInstaller `
        --noconfirm `
        --clean `
        --distpath $outputDirectoryPath `
        --workpath $workDirectoryPath `
        ".\Crea_Report.spec"
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller non ha completato la build (codice $LASTEXITCODE)."
    }

    Write-Host ""
    Write-Host "Eseguibile unico creato in: $executablePath"
}
finally {
    Pop-Location
    if (Test-Path -LiteralPath $workDirectoryPath) {
        Remove-Item -LiteralPath $workDirectoryPath -Recurse -Force -ErrorAction SilentlyContinue
    }
}
