<#
.SYNOPSIS
  One economy refresh as a reviewable PR (plan D7): fetch a snapshot of each named league on
  a new branch from origin/main, validate, commit, push, open one PR. Never commits to main.
.EXAMPLE
  pwsh tools/refresh/run-economy.ps1
  pwsh tools/refresh/run-economy.ps1 -League Covens, "Hardcore Covens", Standard
.NOTES
  League names are poe.ninja league ids; economy.py lists the known ones when a name is wrong.
  SSF leagues have no market, so poe.ninja has no prices for them.
#>
param(
  [string[]]$League = @("Covens"),
  [string]$Repo = (Resolve-Path "$PSScriptRoot\..\..").Path
)
$ErrorActionPreference = "Stop"
Set-Location $Repo
if (git status --porcelain) { throw "working tree not clean: $Repo" }
git fetch -q origin
$date = (Get-Date).ToUniversalTime().ToString("yyyy-MM-dd")
$slugs = $League | ForEach-Object { ($_.ToLower() -replace '[^a-z0-9]+', '-').Trim('-') }
$branch = "refresh/economy-$($slugs -join '-')-$date"
git checkout -q -b $branch origin/main
try {
  foreach ($l in $League) {
    python tools/refresh/economy.py --league $l --date $date
    if ($LASTEXITCODE -ne 0) { throw "economy.py failed for '$l' ($LASTEXITCODE)" }
  }
  python tools/validate/validate.py
  if ($LASTEXITCODE -ne 0) { throw "validation failed" }
  git add plugins/poe1-expert/skills/poe1-economy/snapshots
  $names = $League -join ", "
  git commit -q -m "Economy snapshot: $names, $date"
  git push -q -u origin $branch
  gh pr create --base main --head $branch --title "Economy snapshot: $names, $date" `
    --body "Economy refresh run by hand (tools/refresh/run-economy.ps1). Review the prices and add the hand-written summary (.md) before merging."
}
finally {
  git checkout -q main
}
