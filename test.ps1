

# 中文输出测试
Write-Host ""
Write-Host "===== 中文输出测试 =====" -ForegroundColor Cyan
Write-Host "测试成功！🎉" -ForegroundColor Green
Write-Host "当前时间: $(Get-Date -Format 'yyyy年MM月dd日 HH:mm:ss')"
Write-Host "PowerShell版本: $($PSVersionTable.PSVersion)"
Write-Host "当前编码: $([Console]::OutputEncoding.EncodingName)"
Write-Host ""
Write-Host "提示：如果仍有乱码，请尝试以下方法：" -ForegroundColor Yellow
Write-Host "1. 确保脚本以''格式保存"
Write-Host "2. 右键控制台标题栏 → 属性 → 选择中文字体"
Write-Host "3. 执行: Set-ItemProperty 'HKCU:\Console' -Name 'CodePage' -Value 65001"

# 恢复原始编码（如果需要）
# [Console]::OutputEncoding = $currentEncoding