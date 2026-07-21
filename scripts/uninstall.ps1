$ErrorActionPreference = "Stop"

$CodexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$Dest = Join-Path $CodexRoot "pets\dantino"

if (Test-Path $Dest) {
  Remove-Item -Recurse -Force $Dest
  Write-Host "Removed Dantino from $Dest"
} else {
  Write-Host "Dantino is not installed at $Dest"
}
