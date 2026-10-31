param([ValidateSet('prepare','inspect','setup','api','start','stop','status','pause','resume','reset','memory-status','resolve-unknown')][string]$Action='start', [string]$Session='')
$ErrorActionPreference='Stop'
& "$PSScriptRoot/runtime/akasha-wechat/venv/Scripts/python.exe" -X utf8 "$PSScriptRoot/scripts/akasha.py" $Action --session $Session
exit $LASTEXITCODE
