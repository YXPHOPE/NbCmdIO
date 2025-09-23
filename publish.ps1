<#
.SYNOPSIS
发布包到 PyPI
#>

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 获取当前脚本所在的目录
$scriptPath = $PSScriptRoot

# 切换到该目录
Set-Location -Path $scriptPath

# 检查twine是否安装
if (-not (Get-Command twine -ErrorAction SilentlyContinue)) {
  pip install twine
}

# 发布到PyPI
$files = Get-ChildItem dist -File
if (-not $files) {
  Write-Error "没有找到可发布的文件，请先运行 build.ps1"
  exit 1
}

Write-Host "`n发布包到 PyPI:" -ForegroundColor Cyan
$files | ForEach-Object { Write-Host "  $($_.Name)" }

twine upload dist/*

Write-Host "`n发布完成！" -ForegroundColor Green