param([switch]$KeepTemp)

$ErrorActionPreference = "Stop"
$skillRoot = Split-Path -Parent $PSScriptRoot
$fixtureRoot = Join-Path $skillRoot "evals/portable-repository"
$validatorSource = Join-Path $PSScriptRoot "validate_readme_governance.py"
$lintSource = Join-Path $skillRoot "assets/lint-git-governance.ps1"
$tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
$tempRoot = Join-Path $tempBase ("aicoding-portable-governance-" + [guid]::NewGuid().ToString("N"))
[System.IO.Directory]::CreateDirectory($tempRoot) | Out-Null

function New-Fixture([string]$Name) {
    $destination = Join-Path $tempRoot $Name
    Copy-Item -LiteralPath $fixtureRoot -Destination $destination -Recurse -Force
    Copy-Item -LiteralPath $validatorSource -Destination (Join-Path $destination "scripts/validate_readme_governance.py") -Force
    Copy-Item -LiteralPath $lintSource -Destination (Join-Path $destination "scripts/lint-git-governance.ps1") -Force
    & git -C $destination init --quiet
    if ($LASTEXITCODE -ne 0) { throw "git init failed for $Name" }
    & git -C $destination config user.name "Portable Fixture"
    & git -C $destination config user.email "portable@example.invalid"
    return $destination
}

function Replace-Text([string]$Path, [string]$Old, [string]$New) {
    $text = [System.IO.File]::ReadAllText($Path)
    if (-not $text.Contains($Old)) { throw "Fixture mutation token not found in $Path`: $Old" }
    [System.IO.File]::WriteAllText($Path, $text.Replace($Old, $New))
}

function Invoke-LintCase(
    [string]$Name,
    [bool]$ExpectSuccess,
    [string]$ExpectedToken,
    [scriptblock]$Mutate
) {
    $fixture = New-Fixture $Name
    if ($Mutate) { & $Mutate $fixture }
    $configText = [System.IO.File]::ReadAllText((Join-Path $fixture ".github/repository-governance.toml"))
    $portablePolicy = $configText -match '(?m)^\[readme\.(structure|banner|badges|architecture_graph|capability_showcase|evolution|star_history)\]\s*$'
    if ($portablePolicy) {
        $output = @(& python (Join-Path $fixture "scripts/validate_readme_governance.py") --config ".github/repository-governance.toml" --repo-root $fixture 2>&1)
        $exitCode = $LASTEXITCODE
        if ($exitCode -eq 0) {
            $lintOutput = @(& pwsh -NoProfile -ExecutionPolicy Bypass -File (Join-Path $fixture "scripts/lint-git-governance.ps1") -Mode all 2>&1 3>&1 4>&1 5>&1 6>&1)
            $lintExitCode = $LASTEXITCODE
            if ($lintExitCode -ne 0) { throw "Portable validator passed but full lint failed: $Name`n$($lintOutput -join "`n")" }
            $output += $lintOutput
        }
    }
    else {
        $output = @(& pwsh -NoProfile -ExecutionPolicy Bypass -File (Join-Path $fixture "scripts/lint-git-governance.ps1") -Mode all 2>&1 3>&1 4>&1 5>&1 6>&1)
        $exitCode = $LASTEXITCODE
    }
    $success = $exitCode -eq 0
    $joined = $output -join "`n"
    if ($success -ne $ExpectSuccess) {
        throw "Case $Name exit mismatch: exit=$exitCode`n$joined"
    }
    if ($ExpectedToken -and -not $joined.Contains($ExpectedToken)) {
        throw "Case $Name did not report $ExpectedToken`n$joined"
    }
    if ($Name -eq "legacy-toml-pass" -and $joined.TrimEnd() -cne "Git governance lint passed (all).") {
        throw "Legacy TOML output drifted from the pre-profile byte contract:`n$joined"
    }
    $evidence = @($output | Where-Object { $_ -match 'README-GOV-|Portable README governance passed|Git governance lint passed' })
    $byteExact = $Name -eq "legacy-toml-pass"
    Write-Host "CASE $Name exit=$exitCode expectedToken=$ExpectedToken byteExact=$byteExact"
    $evidence | ForEach-Object { Write-Host $_ }
}

try {
    Invoke-LintCase "portable-pass" $true "Portable README governance passed" $null

    Invoke-LintCase "legacy-toml-pass" $true "Git governance lint passed" {
        param($fixture)
        $path = Join-Path $fixture ".github/repository-governance.toml"
        $text = [System.IO.File]::ReadAllText($path)
        $text = [regex]::Replace($text, '(?ms)^\[readme\.structure\].*?(?=^\[changelog\])', '')
        [System.IO.File]::WriteAllText($path, $text)
    }

    Invoke-LintCase "badge-wrong-version" $false "README-GOV-038" {
        param($fixture)
        foreach ($name in @("README.md", "README_CN.md", "README_EN.md")) {
            Replace-Text (Join-Path $fixture $name) "Go-1.22-00ADD8" "Go-9.99-00ADD8"
        }
    }

    Invoke-LintCase "capability-missing" $false "README-GOV-048" {
        param($fixture)
        Replace-Text (Join-Path $fixture "README.md") '- **Parser** — 把输入转换成结构化结果。[详情](https://example.invalid/portable-service/parser)' ''
    }

    Invoke-LintCase "capability-ghost" $false "README-GOV-050" {
        param($fixture)
        $line = '- **Parser** — 把输入转换成结构化结果。[详情](https://example.invalid/portable-service/parser)'
        $ghost = '- **Ghost** — 未注册能力。[详情](https://example.invalid/portable-service/ghost)'
        Replace-Text (Join-Path $fixture "README.md") $line "$line`n$ghost"
    }

    Invoke-LintCase "quadrants-required" $false "README-GOV-072" {
        param($fixture)
        Replace-Text (Join-Path $fixture "README.md") '<!-- quadrant:unknown-unknown -->' '<!-- quadrant:removed -->'
    }

    Invoke-LintCase "quadrants-recommended" $true "README-GOV-073" {
        param($fixture)
        Replace-Text (Join-Path $fixture ".github/repository-governance.toml") 'quadrants_section = "required"' 'quadrants_section = "recommended"'
        Replace-Text (Join-Path $fixture "README.md") '<!-- quadrant:unknown-unknown -->' '<!-- quadrant:removed -->'
    }

    Invoke-LintCase "star-history-credential" $false "README-GOV-081" {
        param($fixture)
        foreach ($name in @(".github/repository-governance.toml", "README.md")) {
            Replace-Text (Join-Path $fixture $name) 'https://star-history.com/#example/portable-service&Date' 'https://star-history.com/#example/portable-service?token=secret'
        }
    }

    Invoke-LintCase "mermaid-node-budget" $false "README-GOV-062" {
        param($fixture)
        $nodes = 1..18 | ForEach-Object { "    D$_[`"Extra $_`"]" }
        Replace-Text (Join-Path $fixture "README.md") '    C["Result"]' ("    C[`"Result`"]`n" + ($nodes -join "`n"))
    }

    Invoke-LintCase "mermaid-unknown-command" $false "README-GOV-067" {
        param($fixture)
        Replace-Text (Join-Path $fixture "README.md") 'cmd:portable check' 'cmd:portable launch'
    }

    Write-Host "Portable README governance fixture matrix passed."
}
finally {
    if ($KeepTemp) {
        Write-Host "Fixture temp retained: $tempRoot"
    }
    else {
        $resolved = [System.IO.Path]::GetFullPath($tempRoot)
        if (-not $resolved.StartsWith($tempBase, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Refusing to remove fixture directory outside temp: $resolved"
        }
        Remove-Item -LiteralPath $resolved -Recurse -Force
    }
}
