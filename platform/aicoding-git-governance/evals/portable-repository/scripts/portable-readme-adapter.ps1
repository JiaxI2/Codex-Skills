param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("badges", "capabilities", "commands")]
    [string]$Contract,

    [Parameter(Mandatory = $true)]
    [string]$RepoRoot
)

$catalog = Get-Content -Raw -LiteralPath (Join-Path $RepoRoot "config/portable-catalog.json") | ConvertFrom-Json
switch ($Contract) {
    "badges" { [pscustomobject]@{ badges = @($catalog.badges) } | ConvertTo-Json -Depth 5 }
    "capabilities" { [pscustomobject]@{ capabilities = @($catalog.capabilities) } | ConvertTo-Json -Depth 5 }
    "commands" { [pscustomobject]@{ commands = @($catalog.commands) } | ConvertTo-Json -Depth 5 }
}
