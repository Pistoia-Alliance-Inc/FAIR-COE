Param([switch]$FromExamples)
$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
if (-not $FromExamples) {
  $EnvFile = Join-Path $RootDir ".env"
  if (Test-Path $EnvFile) {
    Get-Content $EnvFile | ForEach-Object {
      if ($_ -match "^(.*?)=(.*)$") {
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
      }
    }
  }
  python (Join-Path $RootDir "scripts\checkout_repos.py")
  python (Join-Path $RootDir "scripts\sync_public_docs.py")
  python (Join-Path $RootDir "scripts\generate_site_config.py")
  python (Join-Path $RootDir "scripts\write_promotion_manifest.py")
} else {
  python (Join-Path $RootDir "scripts\sync_public_docs.py") --from-examples
  python (Join-Path $RootDir "scripts\generate_site_config.py") --from-examples
}
