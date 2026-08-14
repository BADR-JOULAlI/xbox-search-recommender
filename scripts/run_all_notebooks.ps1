$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Jupyter = Join-Path $ProjectRoot ".venv\Scripts\jupyter.exe"
$OutputDir = Join-Path $ProjectRoot "reports\executed-notebooks"

if (-not (Test-Path -LiteralPath $Jupyter)) {
    throw "Jupyter introuvable. Installez d'abord l'environnement du projet."
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$Notebooks = Get-ChildItem -LiteralPath (Join-Path $ProjectRoot "notebooks") -Filter "*.ipynb" |
    Sort-Object Name

foreach ($Notebook in $Notebooks) {
    Write-Host "Exécution de $($Notebook.Name)"
    & $Jupyter nbconvert --to notebook --execute $Notebook.FullName `
        --output "$($Notebook.BaseName).executed.ipynb" `
        --output-dir $OutputDir `
        --ExecutePreprocessor.timeout=900
    if ($LASTEXITCODE -ne 0) {
        throw "Échec du notebook $($Notebook.Name)"
    }
}

Write-Host "Tous les notebooks ont été exécutés avec succès."

