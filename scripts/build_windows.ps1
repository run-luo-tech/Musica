param([string]$Python = '', [string]$Iscc = '', [switch]$PortableOnly)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $projectRoot
if (-not $Python) { $Python = Join-Path $projectRoot '.venv\Scripts\python.exe' }
if (-not (Test-Path -LiteralPath $Python)) {
    throw '构建机需要 Python 和 requirements-build.txt；主持人直接使用发行 EXE，无需安装。'
}
$version = & $Python -c 'from src.apps.desktop import APP_VERSION; print(APP_VERSION)'
if ($LASTEXITCODE -ne 0 -or $version -notmatch '^\d+\.\d+\.\d+$') { throw '无法读取发行版本。' }
$releasePath = Join-Path $projectRoot "releases\Musica-Windows-x64-v$version"
$assetRoot = Join-Path $projectRoot 'assets'
& $Python -m PyInstaller --noconfirm --windowed --onefile --name Musica --icon "$assetRoot\Musica.ico" --add-data "${assetRoot}:assets" --distpath $releasePath --workpath build\windows --specpath build run.py
if ($LASTEXITCODE -ne 0) { throw 'PyInstaller 构建失败。' }
Copy-Item -LiteralPath 'packaging\Windows-快速开始.txt','THIRD_PARTY_NOTICES.md' -Destination $releasePath -Force
Copy-Item -LiteralPath 'licenses' -Destination $releasePath -Recurse -Force
$pdfPath = Join-Path $projectRoot 'docs\manual\Musica-使用说明书.pdf'
if (-not (Test-Path -LiteralPath $pdfPath)) { throw '缺少发行说明书，请先构建说明书。' }
Copy-Item -LiteralPath $pdfPath -Destination $releasePath -Force
# Explicit inputs prevent an existing local data/config folder from entering the ZIP.
$publicFiles = @('Musica.exe','Windows-快速开始.txt','THIRD_PARTY_NOTICES.md','Musica-使用说明书.pdf','licenses') |
    ForEach-Object { Join-Path $releasePath $_ }
Compress-Archive -LiteralPath $publicFiles -DestinationPath "$releasePath.zip" -Force
if (-not $PortableOnly) {
    if (-not $Iscc) {
        $candidates = @(
            (Join-Path $projectRoot 'build\tools\InnoSetup\ISCC.exe'),
            "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
            "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe"
        )
        $Iscc = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    }
    if (-not $Iscc) { throw '需要 Inno Setup 6 编译器；通过 -Iscc 指定 ISCC.exe，或用 -PortableOnly 仅构建便携包。' }
    & $Iscc "/DAppVersion=$version" "/DReleaseDir=$releasePath" "/DOutputDir=$projectRoot\releases" 'packaging\windows-installer.iss'
    if ($LASTEXITCODE -ne 0) { throw '安装包编译失败。' }
}
Write-Output "发行目录：$releasePath。只含程序、说明及许可，不包含个人曲库。"
