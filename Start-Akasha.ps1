param([ValidateSet('prepare','inspect','setup','api','start','stop','status','pause','resume','reset','memory-status','resolve-unknown')][string]$Action='start', [string]$Session='')
$ErrorActionPreference='Stop'
$akashaArguments = @('-X', 'utf8', "$PSScriptRoot/scripts/akasha.py", $Action)
if ($Session) { $akashaArguments += @('--session', $Session) }
& "$PSScriptRoot/runtime/akasha-wechat/venv/Scripts/python.exe" @akashaArguments
exit $LASTEXITCODE
