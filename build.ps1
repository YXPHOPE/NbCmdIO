<#
.SYNOPSIS
构建 NbCmdIO 项目并生成分发包
#>

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 获取当前脚本所在的目录
$scriptPath = $PSScriptRoot

# 切换到该目录
Set-Location -Path $scriptPath

# 清理构建目录
Remove-Item -Recurse -Force build, dist, *.egg-info -ErrorAction SilentlyContinue

# 安装依赖
$pipList = python -m pip list --format=json 2>$null
$packages = @('setuptools', 'wheel')
foreach ($package in $packages) {
  if(-not $pipList -match $package){
    Write-Host "$package 正在安装..."
    pip install $package
  }
}

# 构建源码包和wheel包
python setup.py sdist bdist_wheel

# 显示构建结果
Write-Host "`n构建完成！" -ForegroundColor Green
Write-Host "包文件在 dist 目录下："
Get-ChildItem dist | Format-Table Name

# 本地安装测试
$whlFiles = Get-ChildItem -Path .\dist\*.whl
foreach ($whl in $whlFiles) {
  Write-Host "正在安装: $($whl.FullName)"
  pip install $whl.FullName --force-reinstall
}