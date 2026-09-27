param([Parameter(Mandatory=$true)][string]$SourcePath)
$ErrorActionPreference='Stop'
$source=(Resolve-Path $SourcePath).Path
if(-not (Get-Command dotnet -ErrorAction SilentlyContinue)) { throw 'Install the .NET 10 SDK first.' }
if(-not (Get-Command msbuild -ErrorAction SilentlyContinue)) { throw 'Run this in a Visual Studio developer PowerShell with the C++ workload installed.' }
Push-Location $source
try {
  if(-not (Test-Path UI/Dependencies/librashader.dll)) {
    $shaderZip=Join-Path ([System.IO.Path]::GetTempPath()) ('raster-shader-'+[guid]::NewGuid().ToString()+'.zip')
    $shaderDir=$shaderZip+'.contents'
    try {
      Invoke-WebRequest -Uri 'https://nightly.link/SourMesen/librashader/workflows/build/Mesen/librashader-x64-windows.zip' -OutFile $shaderZip -MaximumRedirection 10
      Expand-Archive -Path $shaderZip -DestinationPath $shaderDir
      $shader=Get-ChildItem -Path $shaderDir -File -Filter librashader.dll | Select-Object -First 1
      if($null -eq $shader) { throw 'The upstream shader package does not contain librashader.dll.' }
      Copy-Item $shader.FullName UI/Dependencies/librashader.dll
    } finally {
      Remove-Item $shaderZip -Force -ErrorAction SilentlyContinue
      Remove-Item $shaderDir -Recurse -Force -ErrorAction SilentlyContinue
    }
  }
  dotnet restore -p:TargetFramework=net10.0 -r win-x64 -p:PublishAot=true -p:BuildWithNetFrameworkHostedCompiler=true
  if($LASTEXITCODE -ne 0) { throw 'Restore failed' }
  msbuild -nologo -v:m -m -p:Configuration=Release -p:Platform=x64 '-t:Clean,UI' -p:TargetFramework=net10.0 -p:OptimizeUi=true
  if($LASTEXITCODE -ne 0) { throw 'Build failed' }
  dotnet publish --no-restore -c Release -p:PublishAot=true -p:SelfContained=true -p:PublishSingleFile=false -p:OptimizeUi=true '-p:Platform=Any CPU' -p:TargetFramework=net10.0 -r win-x64 Mesen.sln '/p:PublishProfile=UI\Properties\PublishProfiles\Release.pubxml'
  if($LASTEXITCODE -ne 0) { throw 'Publish failed' }
  Write-Host "Compiled executable: $source\build\TmpReleaseBuild\Mesen.exe"
} finally { Pop-Location }
