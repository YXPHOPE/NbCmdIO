
param (
    [Parameter(Mandatory=$false)]
    [string]$RemoteUrl = "https://github.com/YXPHOPE/NbCmdIO",
    
    [Parameter(Mandatory=$true)]
    [string]$CommitMessage  # 强制要求的提交信息
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 获取当前脚本所在的目录
$scriptPath = $PSScriptRoot

# 切换到该目录
Set-Location -Path $scriptPath

# 检查是否在Git仓库中
try {
    $isGitRepo = git rev-parse --is-inside-work-tree 2>$null
    if (-not $isGitRepo) {
        throw "当前目录不是Git仓库"
    }
} catch {
    # 如果不是Git仓库，则初始化新仓库
    git init
    
    # 如果没有提供远程URL，提示用户输入
    if ([string]::IsNullOrWhiteSpace($RemoteUrl)) {
        $RemoteUrl = Read-Host "⚠️ 请输入远程仓库URL"
    }
    
    # 添加远程仓库
    git remote add origin $RemoteUrl
    Write-Host "✅ 已添加远程仓库: $RemoteUrl"
}

# 获取当前分支名称
$currentBranch = git rev-parse --abbrev-ref HEAD

# 添加所有更改
git add -A 2>&1 | Out-Null
$status = git status --porcelain
if ($status) {
    Write-Host "✅ 已添加以下文件到暂存区:"
    $status | ForEach-Object { Write-Host "   $($_.Substring(3))" }
} else {
    Write-Host "ℹ️ 没有检测到文件更改"
    exit
}

# 提交更改
try {
    git commit -m $CommitMessage
    Write-Host "✅ 已提交更改: `"$CommitMessage`""
} catch {
    Write-Host "❌ 提交失败: $_"
    exit 1
}

# 推送到远程仓库
try {
    Write-Host "🚀 正在推送到远程仓库 ($currentBranch 分支)..."
    git push -u origin $currentBranch
    Write-Host "✅ 推送成功!"
} catch {
    Write-Host "❌ 推送失败: $_"
    exit 1
}