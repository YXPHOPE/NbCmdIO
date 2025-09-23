<#
.SYNOPSIS
构建 NbCmdIO 项目并生成分发包
#>

# 清理构建目录
Remove-Item -Recurse -Force build, dist, *.egg-info -ErrorAction SilentlyContinue

# 安装依赖
python -m pip install --upgrade pip setuptools wheel

# 构建源码包和wheel包
python setup.py sdist bdist_wheel

# 显示构建结果
Write-Host "`n构建完成！" -ForegroundColor Green
Write-Host "包文件在 dist 目录下："
Get-ChildItem dist | Format-Table Name