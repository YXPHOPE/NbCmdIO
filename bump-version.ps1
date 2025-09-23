<#
.SYNOPSIS
更新项目版本号
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$NewVersion
)


[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 获取当前脚本所在的目录
$scriptPath = $PSScriptRoot

# 切换到该目录
Set-Location -Path $scriptPath

# 更新 __init__.py 中的版本号
$initFile = "nbcmdio\__init__.py"
(Get-Content $initFile) -replace '__version__ = ".*"', "__version__ = `"$NewVersion`"" | Set-Content $initFile
$outputFile = "nbcmdio\output.py"
(Get-Content $outputFile) -replace '__version__ = ".*"', "__version__ = `"$NewVersion`"" | Set-Content $outputFile

# 更新 setup.py 中的版本号
$setupFile = "setup.py"
(Get-Content $setupFile) -replace 'version=".*"', "version=`"$NewVersion`"" | Set-Content $setupFile

Write-Host "版本号已更新为 $NewVersion" -ForegroundColor Green
