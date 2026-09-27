param([string]$ApplicationPath, [string]$OutputPath)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
$env:RASTER_SOUND_PREVIEW='1'
$app=(Resolve-Path $ApplicationPath).Path
$started=Get-Date
$diagnostics=Join-Path (Split-Path $app -Parent) 'StartupDiagnostics'
New-Item -ItemType Directory -Force $diagnostics | Out-Null
Get-CimInstance Win32_SoundDevice | Format-List Name,Status | Out-File (Join-Path $diagnostics 'audio-devices.txt')
$process=Start-Process -FilePath $app -WorkingDirectory (Split-Path $app -Parent) -RedirectStandardOutput (Join-Path $diagnostics 'stdout.txt') -RedirectStandardError (Join-Path $diagnostics 'stderr.txt') -PassThru
try {
  Start-Sleep -Seconds 12
  if($process.HasExited) {
    Get-WinEvent -FilterHashtable @{LogName='Application'; StartTime=$started} -ErrorAction SilentlyContinue | Select-Object TimeCreated,ProviderName,Id,Message | Format-List | Out-File (Join-Path $diagnostics 'windows-events.txt')
    throw "Raster exited before UI capture: $($process.ExitCode)"
  }
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
