$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Kaggle = Join-Path $ProjectRoot ".venv\Scripts\kaggle.exe"
$RawDir = Join-Path $ProjectRoot "data\raw"

if (-not (Test-Path -LiteralPath $Kaggle)) {
    throw "Kaggle CLI introuvable. Installez d'abord l'environnement du projet."
}

New-Item -ItemType Directory -Force -Path $RawDir | Out-Null
& $Kaggle competitions download -c acm-sf-chapter-hackathon-small -p $RawDir

if ($LASTEXITCODE -ne 0) {
    throw "Téléchargement refusé. Vérifiez l'authentification et acceptez les règles du challenge."
}

Write-Host "Données téléchargées dans $RawDir"

