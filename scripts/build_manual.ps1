$ErrorActionPreference = 'Stop'
$manualRoot = Join-Path (Split-Path $PSScriptRoot -Parent) 'docs\manual'
Push-Location -LiteralPath $manualRoot
try {
    New-Item -ItemType Directory -Force -Path build | Out-Null
    1..2 | ForEach-Object {
        & xelatex -interaction=nonstopmode -halt-on-error -output-directory=build 'Musica-使用说明书.tex'
        if ($LASTEXITCODE -ne 0) { throw 'XeLaTeX 编译失败。' }
    }
    Copy-Item -LiteralPath 'build\Musica-使用说明书.pdf' -Destination 'Musica-使用说明书.pdf' -Force
} finally { Pop-Location }
