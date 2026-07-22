param([string]$RepoRoot = (Split-Path -Parent $PSScriptRoot))

$assetRoot = Join-Path $RepoRoot "docs/assets"
[System.IO.Directory]::CreateDirectory($assetRoot) | Out-Null
[System.IO.File]::WriteAllText((Join-Path $assetRoot "banner-light.svg"), '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="120"><rect width="640" height="120" fill="#ffffff"/><text x="32" y="72" fill="#111827">Portable Service</text></svg>')
[System.IO.File]::WriteAllText((Join-Path $assetRoot "banner-dark.svg"), '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="120"><rect width="640" height="120" fill="#111827"/><text x="32" y="72" fill="#f9fafb">Portable Service</text></svg>')
