param([switch]$Json)
$ErrorActionPreference = 'Stop'
$repoRoot = (& git -C $PSScriptRoot rev-parse --show-toplevel).Trim()
$errors = New-Object System.Collections.Generic.List[string]
$skillFiles = @(Get-ChildItem -LiteralPath $repoRoot -Recurse -Filter SKILL.md | Where-Object {
    $_.FullName -notmatch '\\.system\\' -and $_.FullName -notmatch '\\plugins\\AiCoding\\skills\\'
})
foreach ($file in $skillFiles) {
    $text = ([System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)).TrimStart([char]0xFEFF)
    if ($text -notmatch '(?s)^---\s*\r?\n.*?\r?\n---') { $errors.Add("Missing frontmatter: $($file.FullName)") | Out-Null }
    if ($text -notmatch '(?m)^name:\s*[^\r\n]+') { $errors.Add("Missing name: $($file.FullName)") | Out-Null }
    if ($text -notmatch '(?m)^description:\s*') { $errors.Add("Missing description: $($file.FullName)") | Out-Null }
}
if ($Json) { [pscustomobject]@{ ok=($errors.Count -eq 0); count=$skillFiles.Count; errors=$errors } | ConvertTo-Json -Depth 5 } elseif ($errors.Count -eq 0) { Write-Host "Skill verification passed ($($skillFiles.Count) SKILL.md files)." } else { $errors | ForEach-Object { Write-Error $_ } }
if ($errors.Count -gt 0) { exit 1 }