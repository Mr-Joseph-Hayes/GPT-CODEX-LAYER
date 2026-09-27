param([string]$ApplicationPath, [string]$OutputPath)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
$env:RASTER_SOUND_PREVIEW='1'
$app=(Resolve-Path $ApplicationPath).Path
$process=Start-Process -FilePath $app -PassThru
try {
  Start-Sleep -Seconds 12
  if($process.HasExited) { throw "Raster exited before UI capture: $($process.ExitCode)" }
  $bounds=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds
  $bitmap=New-Object System.Drawing.Bitmap $bounds.Width,$bounds.Height
  $graphics=[System.Drawing.Graphics]::FromImage($bitmap)
  $graphics.CopyFromScreen($bounds.Location,[System.Drawing.Point]::Empty,$bounds.Size)
  $bitmap.Save((Join-Path (Get-Location) $OutputPath),[System.Drawing.Imaging.ImageFormat]::Png)
  $graphics.Dispose(); $bitmap.Dispose()
  $process.CloseMainWindow() | Out-Null
  if(-not $process.WaitForExit(5000)) { Stop-Process -Id $process.Id }
} finally {
  if(-not $process.HasExited) { Stop-Process -Id $process.Id }
  Remove-Item Env:RASTER_SOUND_PREVIEW
}
