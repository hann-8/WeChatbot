param([switch]$Live)
$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
$pythonPath = Join-Path $projectRoot '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw 'Project Python missing. Prepare the project .venv first.'
}
Push-Location $projectRoot
try {
    if ($Live) { & $pythonPath -m wechatbot.wxauto4_chat --live }
    else { & $pythonPath -m wechatbot.wxauto4_chat }
    if ($LASTEXITCODE -ne 0) { throw 'WeChatbot stopped with an error.' }
} finally { Pop-Location }
