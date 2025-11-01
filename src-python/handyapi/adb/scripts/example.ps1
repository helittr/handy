[console]::OutputEncoding = New-Object System.Text.UTF8Encoding

try {
    # 主循环检测标志
    while (-not $global:exitFlag) {
        Write-Host "运行中..."
        write-host "你好啊，世界！"
        write-host "This is an example script for windows PowerShell."
        write-host "Parameters: $args"
        write-host "Start Current Date and Time: $(Get-Date)"
        write-host "End Current Date and Time: $(Get-Date)"
        write-host "你好啊，世界！"
        Start-Sleep -Seconds 1
    }
}
catch {
    Write-Host "正在释放资源..."
    if ($_.Exception -is [System.Management.Automation.PipelineStoppedException]) {
        Write-Host "Exception"  $_.Exception
    }
}


