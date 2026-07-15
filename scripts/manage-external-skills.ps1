param(
    [ValidateSet('Status', 'Sync', 'Remove')]
    [string]$Action = 'Status',
    [string]$Name,
    [switch]$Apply,
    [switch]$Json
)

$ErrorActionPreference = 'Stop'
$repoRoot = (& git -C $PSScriptRoot rev-parse --show-toplevel).Trim()
$configPath = Join-Path $repoRoot 'config/external-skill-bindings.json'
$config = Get-Content -Raw -LiteralPath $configPath | ConvertFrom-Json
$bindings = @($config.skills)

if ($Name) {
    $bindings = @($bindings | Where-Object { $_.name -eq $Name })
    if ($bindings.Count -eq 0) { throw "External Skill binding not found: $Name" }
}
if ($Action -eq 'Remove' -and -not $Name) { throw '-Name is required for Remove.' }

function Get-LatestStableTag {
    param([string]$Repository, [string]$Pattern)
    $candidates = @()
    foreach ($tag in @(& git -C $Repository tag --list)) {
        if ($tag -notmatch $Pattern) { continue }
        try {
            $candidates += [pscustomobject]@{ tag = $tag; version = [version]($tag -replace '^[vV]','') }
        } catch { }
    }
    $latest = $candidates | Sort-Object version -Descending | Select-Object -First 1
    if (-not $latest) { throw "No stable semantic-version tag matches '$Pattern' in $Repository" }
    return $latest.tag
}

$results = @()
foreach ($binding in $bindings) {
    $submodule = ([string]$binding.submodule -replace '\\','/').TrimEnd('/')
    $submoduleDir = Join-Path $repoRoot $submodule

    if ($Action -eq 'Remove') {
        $results += [pscustomobject]@{
            name = $binding.name
            action = 'remove'
            apply = [bool]$Apply
            submodule = $submodule
            removes = @('binding manifest entry', '.gitmodules section', 'tracked gitlink')
        }
        if ($Apply) {
            & git -C $repoRoot submodule deinit -f -- $submodule | Out-Null
            $moduleRow = @(& git -C $repoRoot config -f .gitmodules --get-regexp '^submodule\..*\.path$' | Where-Object { $_ -match ('\s' + [regex]::Escape($submodule) + '$') }) | Select-Object -First 1
            if (-not $moduleRow) { throw "Submodule declaration not found: $submodule" }
            $section = (($moduleRow -split '\s+', 2)[0] -replace '\.path$','')
            & git -C $repoRoot config -f .gitmodules --remove-section $section
            & git -C $repoRoot rm -f -- $submodule | Out-Null
            $config.skills = @($config.skills | Where-Object { $_.name -ne $binding.name })
            $text = ($config | ConvertTo-Json -Depth 10) + "`n"
            [System.IO.File]::WriteAllText($configPath, $text, (New-Object System.Text.UTF8Encoding $false))
            & git -C $repoRoot add -- .gitmodules config/external-skill-bindings.json
        }
        continue
    }

    if (-not (Test-Path -LiteralPath $submoduleDir)) { throw "Submodule is not initialized: $submodule" }
    if ($Action -eq 'Sync') { & git -C $submoduleDir fetch --tags --prune origin | Out-Null }
    $latestTag = Get-LatestStableTag -Repository $submoduleDir -Pattern ([string]$binding.tagPattern)
    $latestCommit = (& git -C $submoduleDir rev-list -n 1 $latestTag).Trim()
    $currentCommit = (& git -C $submoduleDir rev-parse HEAD).Trim()
    $currentTags = @(& git -C $submoduleDir tag --points-at HEAD | Where-Object { $_ -match [string]$binding.tagPattern })
    $changed = $currentCommit -ne $latestCommit
    $updated = $false
    if ($Action -eq 'Sync' -and $Apply -and $changed) {
        & git -C $submoduleDir checkout --detach $latestTag | Out-Null
        & git -C $repoRoot add -- $submodule
        $currentCommit = (& git -C $submoduleDir rev-parse HEAD).Trim()
        $currentTags = @(& git -C $submoduleDir tag --points-at HEAD | Where-Object { $_ -match [string]$binding.tagPattern })
        $changed = $currentCommit -ne $latestCommit
        $updated = $true
    }
    $results += [pscustomobject]@{
        name = $binding.name
        action = $Action.ToLowerInvariant()
        apply = [bool]$Apply
        currentTag = if ($currentTags.Count -gt 0) { $currentTags[0] } else { $null }
        latestStableTag = $latestTag
        currentCommit = $currentCommit
        latestCommit = $latestCommit
        updateAvailable = $changed
        updated = $updated
    }
}

if ($Json) { $results | ConvertTo-Json -Depth 6 } else { $results | Format-Table -AutoSize }
