param(
    [ValidateSet("all", "pre-commit", "commit-msg")]
    [string]$Mode = "all",

    [string]$CommitMsgPath = ""
)

$ErrorActionPreference = "Stop"

function Fail([string]$Message) {
    Write-Error $Message
    exit 1
}

function Require-Content([string]$Path, [string]$Pattern, [string]$Message) {
    $content = Get-Content -LiteralPath $Path -Raw -Encoding utf8
    if ($content -notmatch $Pattern) {
        Fail $Message
    }
}

function Get-TomlSection([string]$Content, [string]$SectionName) {
    $pattern = "(?ms)^\[$([regex]::Escape($SectionName))\]\s*(.*?)(?=^\[|\z)"
    if ($Content -match $pattern) { return $Matches[1] }
    return ""
}

function Get-TomlStringValue([string]$SectionContent, [string]$Key) {
    $pattern = "(?m)^$([regex]::Escape($Key))\s*=\s*`"([^`"]+)`""
    if ($SectionContent -match $pattern) { return $Matches[1] }
    return ""
}

function Require-ReadmeHeading([string]$Path, [string]$Heading) {
    Require-Content $Path "(?m)^##\s+$([regex]::Escape($Heading))\s*$" "$Path must include the '$Heading' section required by the selected README profile."
}

$repoRoot = (& git rev-parse --show-toplevel).Trim()
if (-not $repoRoot) { Fail "Not inside a Git repository." }
Set-Location $repoRoot

$requiredFiles = @(
    "README.md",
    "CHANGELOG.md",
    ".github/repository-governance.toml",
    ".githooks/pre-commit",
    ".githooks/commit-msg"
)

foreach ($file in $requiredFiles) {
    if (-not (Test-Path -LiteralPath $file)) {
        Fail "Required governance file missing: $file"
    }
}

$governance = Get-Content -LiteralPath ".github/repository-governance.toml" -Raw -Encoding utf8
$readmeSection = Get-TomlSection $governance "readme"
$readmeProfile = Get-TomlStringValue $readmeSection "profile"
$changelogSection = Get-TomlSection $governance "changelog"
$changelogMode = Get-TomlStringValue $changelogSection "mode"

$scanFiles = @("README.md", "CHANGELOG.md", ".github/repository-governance.toml")
foreach ($file in $scanFiles) {
    $content = Get-Content -LiteralPath $file -Raw -Encoding utf8
    if ($content -match "\{\{[^}]+\}|UNRESOLVED_PLACEHOLDER|TODO_PLACEHOLDER") {
        Fail "Unresolved placeholder found in $file"
    }
}

if (Test-Path -LiteralPath "README_CN.md") {
    Require-Content "README.md" "README_CN\.md" "README.md must include a visible top-of-file link to README_CN.md when README_CN.md exists."
    Require-Content "README_CN.md" "README\.md" "README_CN.md must include a visible top-of-file link to README.md when README.md exists."
}

if ($readmeProfile -eq "minimal-internal") {
    $englishHeadings = @(
        "Repository Role",
        "Status",
        "Quick Start",
        "Directory Guide",
        "Build And Verify",
        "Documentation And Support",
        "Changelog And Releases"
    )
    foreach ($heading in $englishHeadings) { Require-ReadmeHeading "README.md" $heading }

    if (Test-Path -LiteralPath "README_CN.md") {
        $chineseHeadings = @(
            "仓库定位",
            "状态",
            "快速开始",
            "目录说明",
            "构建和验证",
            "文档和支持",
            "更新日志和发布"
        )
        foreach ($heading in $chineseHeadings) { Require-ReadmeHeading "README_CN.md" $heading }
    }
}

Require-Content "README.md" "Git Governance Standard|Git 治理标准" "README.md must document the Git governance standard: branch/environment, commit types, single-commit rules, and release typed summaries."
Require-Content "README.md" "feat.+fix.+docs.+style.+refactor.+perf.+test.+chore|feat.+fix.+docs.+build.+ci.+chore" "README.md must document the standard commit type taxonomy."
Require-Content "README.md" "main.+master.+develop.+feature.+test.+release.+hotfix|main.+develop.+feature.+test.+release.+hotfix" "README.md must document branch naming and environment mapping."
Require-Content "README.md" "Release.+type|Release.+typed|按类型汇总|主类型" "README.md must document that Release notes group commits by type and state the primary release type."

$localPathFragments = @(
    "C:\Users",
    "F:\Study",
    "AppData\Local\Temp"
)

$readmeFiles = @("README.md")
if (Test-Path -LiteralPath "README_CN.md") { $readmeFiles += "README_CN.md" }
foreach ($file in $readmeFiles) {
    $content = Get-Content -LiteralPath $file -Raw -Encoding utf8
    foreach ($fragment in $localPathFragments) {
        if ($content.Contains($fragment)) {
            Fail "README files must not hard-code personal local paths: $file"
        }
    }
}

if (Test-Path -LiteralPath "README_CN.md") {
    Require-Content "README_CN.md" "Git 治理标准|Git Governance Standard" "README_CN.md must document the Git governance standard when it exists."
    Require-Content "README_CN.md" "feat.+fix.+docs.+style.+refactor.+perf.+test.+chore|feat.+fix.+docs.+build.+ci.+chore" "README_CN.md must document the standard commit type taxonomy."
    Require-Content "README_CN.md" "main.+master.+develop.+feature.+test.+release.+hotfix|main.+develop.+feature.+test.+release.+hotfix" "README_CN.md must document branch naming and environment mapping."
    Require-Content "README_CN.md" "Release.+主类型|按类型汇总|Release.+typed" "README_CN.md must document that Release notes group commits by type and state the primary release type."
}

$changelog = Get-Content -LiteralPath "CHANGELOG.md" -Raw -Encoding utf8
if ($changelogMode -eq "unreleased" -and $changelog -notmatch "\[Unreleased\]") {
    Fail "CHANGELOG.md must contain [Unreleased] when changelog.mode is unreleased."
}
if ($changelog -notmatch "\*\*(feat|fix|docs|style|refactor|perf|test|build|ci|chore)(\([^)]*\))?\*\*") {
    Fail "CHANGELOG.md must include typed entries such as **docs** or **chore**."
}

if ($Mode -eq "all" -or $Mode -eq "pre-commit") {
    $staged = @(& git diff --cached --name-only --diff-filter=ACMR)
    if ($staged.Count -gt 0 -and -not ($staged -contains "CHANGELOG.md")) {
        if ($env:AICODING_SKIP_CHANGELOG -ne "1") {
            Fail "CHANGELOG.md must be staged for normal commits. Set AICODING_SKIP_CHANGELOG=1 only for an approved exclusion."
        }
    }
}

if ($Mode -eq "commit-msg") {
    if (-not $CommitMsgPath) { Fail "Commit message path is required." }
    $subject = (Get-Content -LiteralPath $CommitMsgPath -Encoding utf8 | Where-Object { $_ -and -not $_.StartsWith("#") } | Select-Object -First 1)
    if (-not $subject) { Fail "Commit message subject is empty." }
    $pattern = "^(feat|fix|docs|style|refactor|perf|test|build|ci|chore)(\([a-z0-9._/-]+\))?: .{8,}$"
    if ($subject -notmatch $pattern) {
        Fail "Commit subject must match <type>(<scope>): <summary>. Got: $subject"
    }
}

Write-Host "Git governance lint passed ($Mode)."
