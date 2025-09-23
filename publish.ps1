<#
.SYNOPSIS
发布包到 PyPI
#>

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