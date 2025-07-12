[console]::OutputEncoding = New-Object System.Text.UTF8Encoding

write-host "你好啊，世界！"

write-host "This is an example script for windows PowerShell."

write-host "Parameters: $args"

Get-ChildItem Env:

write-host "Start Current Date and Time: $(Get-Date)"

$cnt = 0

while ($cnt -lt 100) {
    write-host "Current Count: $cnt"
    Start-Sleep -Milliseconds  100
    $cnt++
}

write-host "End Current Date and Time: $(Get-Date)"

write-host "你好啊，世界！"
