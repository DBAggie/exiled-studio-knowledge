<#
.SYNOPSIS
  One economy refresh as a reviewable PR (plan D7): fetch a snapshot on a new branch from
  origin/main, validate, commit, push, open a PR. Never commits to main.
.EXAMPLE
  pwsh tools/refresh/run-economy.ps1 -League Covens
#>
param(
  [string]$League = "Covens",
  [string]$Repo = (Resolve-Path "$PSScriptRoot\..\..").Path
)
$ErrorActionPreference = "Stop"
Set-Location $Repo
if (git status --porcelain) { throw "working tree not clean: $Repo" }
git fetch -q origin
$date = (Get-Date).ToUniversalTime().ToString("yyyy-MM-dd")
$branch = "refresh/economy-$($League.ToLower() -replace '[^a-z0-9]+','-')-$date"
git checkout -q -b $branch origin/main
python tools/refresh/economy.py --league $League --date $date
if ($LASTEXITCODE -ne 0) { throw "economy.py failed ($LASTEXITCODE)" }
python tools/validate/validate.py
if ($LASTEXITCODE -ne 0) { throw "validation failed" }
git add plugins/poe1-expert/skills/poe1-economy/snapshots
git commit -q -m "Economy snapshot: $League, $date"
git push -q -u origin $branch
gh pr create --base main --head $branch --title "Economy snapshot: $League, $date" `
  --body "Scheduled economy refresh (tools/refresh/run-economy.ps1). Review the prices and add the hand-written summary (.md) before merging."
git checkout -q main
