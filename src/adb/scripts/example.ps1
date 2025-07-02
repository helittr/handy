write-host "你好啊，世界！"

write-host "This is an example script for PowerShell."
# 输出所有参数
write-host "Parameters: $args"
# 输出当前日期和时间    
write-host "Start Current Date and Time: $(Get-Date)"

Start-Sleep 10

write-host "End Current Date and Time: $(Get-Date)"

write-host "你好啊，世界！"
