$ErrorActionPreference = "Stop"

$RepoDir = Split-Path -Parent $PSScriptRoot
$CodexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$Dest = Join-Path $CodexRoot "pets\dantino"

New-Item -ItemType Directory -Force -Path $Dest | Out-Null
Copy-Item (Join-Path $RepoDir "package\pet.json") (Join-Path $Dest "pet.json") -Force
Copy-Item (Join-Path $RepoDir "package\spritesheet.webp") (Join-Path $Dest "spritesheet.webp") -Force

Write-Host "Installed Dantino to $Dest"
Write-Host "Refresh or restart Codex if the pet does not appear immediately."
