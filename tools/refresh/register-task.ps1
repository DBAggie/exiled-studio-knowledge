<#
.SYNOPSIS
  Register the economy refresh as a Windows scheduled task on the maintainer's workstation
  (plan D7). Run by the maintainer, once; it changes the machine's task list.
  League-start week: -EveryDays 1 or 2. After that: -EveryDays 7 to 14. Unregister at league end:
    Unregister-ScheduledTask -TaskName "Exiled Studio economy refresh" -Confirm:$false
#>
param(
  [string]$League = "Covens",
  [int]$EveryDays = 2,
  [string]$At = "06:00"
)
$script = Join-Path $PSScriptRoot "run-economy.ps1"
$action = New-ScheduledTaskAction -Execute "pwsh.exe" -Argument "-NoProfile -File `"$script`" -League `"$League`""
$trigger = New-ScheduledTaskTrigger -Daily -DaysInterval $EveryDays -At $At
$settings = New-ScheduledTaskSettingsSet -RunOnlyIfNetworkAvailable -StartWhenAvailable
Register-ScheduledTask -TaskName "Exiled Studio economy refresh" -Action $action -Trigger $trigger -Settings $settings -Description "poe.ninja economy snapshot as a PR to exiled-studio-knowledge" -Force
