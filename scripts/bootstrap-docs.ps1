Param([switch]$FromExamples)
$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
python (Join-Path $RootDir "scripts\check_workflow_actions.py")
