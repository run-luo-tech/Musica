param([string]$Python = '')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $projectRoot
if (-not $Python) { $Python = Join-Path $projectRoot '.venv\Scripts\python.exe' }
if (-not (Test-Path -LiteralPath $Python)) {
    throw '构建机需要 Python 和 requirements-build.txt；主持人直接使用发行 EXE，无需安装。'
}
$releasePath = Join-Path $projectRoot 'releases\Musica-Windows-x64-v0.2.0'
& $Python -m PyInstaller --noconfirm --windowed --onefile --name Musica --distpath $releasePath --workpath build\windows --specpath build run.py
if ($LASTEXITCODE -ne 0) { throw 'PyInstaller 构建失败。' }
Copy-Item -LiteralPath 'packaging\Windows-快速开始.txt','THIRD_PARTY_NOTICES.md' -Destination $releasePath -Force
$pdfPath = Join-Path $projectRoot 'docs\manual\Musica-使用说明书.pdf'
if (Test-Path -LiteralPath $pdfPath) { Copy-Item -LiteralPath $pdfPath -Destination $releasePath -Force }
Write-Output "发行目录：$releasePath。只含程序、说明及许可，不包含个人曲库。"
