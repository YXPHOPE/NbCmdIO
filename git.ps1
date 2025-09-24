# Git 自动提交推送脚本
# 功能：
# 1. 检查是否有未提交的更改
# 2. 如果有则添加所有更改并提示输入提交信息
# 3. 检查本地提交是否已推送
# 4. 如果有未推送的提交则推送到远程

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 获取当前脚本所在的目录
$scriptPath = $PSScriptRoot

# 切换到该目录
Set-Location -Path $scriptPath

# 检查是否在Git仓库中
if (-not (Test-Path ".\.git")) {
    Write-Host "❌ 错误：当前目录不是Git仓库" -ForegroundColor Red
    exit 1
}

# 函数：检查是否有未提交的更改
function HasUncommittedChanges {
    $status = git status --porcelain
    return -not [string]::IsNullOrWhiteSpace($status)
}

# 函数：检查是否有未推送的提交（修复版）
function HasUnpushedCommits {
    # 获取当前分支名
    $branch = git rev-parse --abbrev-ref HEAD
    
    # 计算本地领先于远程的提交数量
    $localCommits = git rev-list $branch --not --remotes --count
    return [int]$localCommits -gt 0
}

# 主流程
Write-Host "`n===== Git 仓库状态检查 =====" -ForegroundColor Cyan

# 检查未提交更改
if (HasUncommittedChanges) {
    Write-Host "📝 检测到未提交的更改：" -ForegroundColor Yellow
    git status -s
    
    # 添加所有更改
    git add -A
    Write-Host "`n✅ 已添加所有更改到暂存区" -ForegroundColor Green
    
    # 获取提交信息
    $commitMessage = Read-Host "`n💬 请输入提交信息 (按Ctrl+C取消)"
    
    if (-not [string]::IsNullOrWhiteSpace($commitMessage)) {
        # 执行提交
        git commit -m $commitMessage
        Write-Host "`n✅ 提交成功！" -ForegroundColor Green
    } else {
        Write-Host "❌ 未输入提交信息，取消提交" -ForegroundColor Red
        exit 2
    }
} else {
    Write-Host "✅ 工作区干净，没有未提交的更改" -ForegroundColor Green
}

# 检查未推送提交
if (HasUnpushedCommits) {
    Write-Host "`n🚀 检测到未推送的提交，正在推送..." -ForegroundColor Yellow
    
    # 获取当前分支名
    $branch = git rev-parse --abbrev-ref HEAD
    
    # 执行推送
    git push origin $branch
    
    if ($?) {
        Write-Host "`n✅ 推送成功！" -ForegroundColor Green
    } else {
        Write-Host "`n❌ 推送失败！请检查网络连接或远程仓库权限" -ForegroundColor Red
        exit 3
    }
} else {
    Write-Host "`n✅ 所有提交已同步到远程仓库" -ForegroundColor Green
}

Write-Host "`n===== 操作完成 =====" -ForegroundColor Cyan