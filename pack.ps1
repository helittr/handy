
$HANDY_VERSION = "0.6.0"

$PYTHON_VERSION = "3.12.9"
$HANDY_ZIP = "handy-0_6_0.zip"


$outDir = "$PSScriptRoot\out"
$handyExe = "$PSScriptRoot\src-tauri\target\release\handy.exe"
$handyServe = "$PSScriptRoot\src-python\dist\handyapi-$HANDY_VERSION-py3-none-any.whl"

$python = "python-$PYTHON_VERSION-embed-amd64.zip"
$embedPythonUrl = "https://mirrors.huaweicloud.com/python/$PYTHON_VERSION/$python"

if ( -not $(Test-Path -Path  $outDir -PathType Container) ) {
    Write-Host "create output directory: $outDir"
    New-Item -Path $outDir -ItemType Directory > $null
    New-Item -Path $outDir/handy -ItemType Directory > $null
}
else {
    Write-Host "output directory: $outDir"
}

if ( -not $(Test-Path -Path "$outDir/$python" -PathType Leaf) ) {
    Write-Host "Download $python from $embedPython"
    Invoke-WebRequest -Uri $embedPythonUrl -OutFile "$outDir/$python"

    # $outPython = Get-ChildItem "$outDir/$python"
    Write-Host "unzip $outDir/$python"
    Expand-Archive -Path "$outDir/$python" -DestinationPath "$outDir/handy/python" -Force
    # Write-Host "delete $outDir/$python"
    # Write-Output "Lib/site-packages" | Out-File -FilePath "$outDir/handy/python/python312._pth" -Append -Encoding utf8
}


uv pip install --python-version $PYTHON_VERSION --python-platform windows --target "$outDir/handy/python" $handyServe -i "https://mirrors.aliyun.com/pypi/simple/" --reinstall-package handyapi --python "$outDir/handy/python/python.exe" --link-mode=copy


Copy-Item -Path $handyExe -Destination $outDir/handy

if ( $(Test-Path -Path "$outDir/$HANDY_ZIP" -PathType Leaf) ) {
    Remove-Item -Path $outDir/$HANDY_ZIP
}

Compress-Archive -Path $outDir/handy -DestinationPath "$outDir/$HANDY_ZIP"
