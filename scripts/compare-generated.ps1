param()
$ErrorActionPreference = 'Stop'
$repoRoot = (& git -C $PSScriptRoot rev-parse --show-toplevel).Trim()
$before = (& git -C $repoRoot status --porcelain)
& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repoRoot 'scripts/build-plugin.ps1') -Plugin AiCoding -Configuration Development -Clean
$after = (& git -C $repoRoot status --porcelain)
if (($before -join "`n") -ne ($after -join "`n")) {
    Write-Error 'Generated plugin output drifted after rebuild.'
    exit 1
}
Write-Host 'Generated plugin output is stable.'