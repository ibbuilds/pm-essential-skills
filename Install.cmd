@echo off
setlocal
set "PM_ESSENTIAL_ROOT=%~dp0"
set "PM_ESSENTIAL_MODE=install"
set "PM_ESSENTIAL_PAUSE=0"
if not "%~2"=="" (
  echo Extra arguments are not supported by Install.cmd. Use scripts/install_suite.py for advanced options.
  exit /b 2
)
if "%~1"=="" set "PM_ESSENTIAL_PAUSE=1"
if /I "%~1"=="status" set "PM_ESSENTIAL_MODE=status"
if /I "%~1"=="uninstall" set "PM_ESSENTIAL_MODE=uninstall"
if not "%~1"=="" if /I not "%~1"=="install" if /I not "%~1"=="status" if /I not "%~1"=="uninstall" (
  echo Usage: Install.cmd [install^|status^|uninstall]
  exit /b 2
)
powershell.exe -NoProfile -Command "$ErrorActionPreference='Stop'; $taskCandidates=@(); $taskBundled=Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'; if(Test-Path -LiteralPath $taskBundled){$taskCandidates+=@{exe=$taskBundled;prefix=@()}}; foreach($taskName in @('python','python3','py')){$taskCommand=Get-Command $taskName -ErrorAction SilentlyContinue; if($taskCommand){$taskCandidates+=@{exe=$taskCommand.Source;prefix=@()}; if($taskName -eq 'py'){$taskCandidates[-1].prefix=@('-3')}}}; $taskPython=$null; foreach($taskCandidate in $taskCandidates){try{$taskPrefix=$taskCandidate.prefix; & $taskCandidate.exe @taskPrefix -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>$null; if($LASTEXITCODE -eq 0){$taskPython=$taskCandidate;break}}catch{}}; if(!$taskPython){Write-Host 'No usable Python runtime was found. Install Codex desktop or Python 3.10+, then open this installer again.';exit 2}; Write-Host 'PM Essential Skills'; if($env:PM_ESSENTIAL_MODE -eq 'install'){Write-Host 'Installing the included skills and their automatic user-level guidance. Existing settings are preserved.'}; $taskPrefix=$taskPython.prefix; $taskOutput=& $taskPython.exe @taskPrefix (Join-Path $env:PM_ESSENTIAL_ROOT 'scripts\install_suite.py') $env:PM_ESSENTIAL_MODE; $taskExit=$LASTEXITCODE; if($taskExit -ne 0){Write-Host 'The operation could not finish. Existing customizations were preserved. Details:'; Write-Host $taskOutput;exit $taskExit}; $taskResult=$taskOutput|ConvertFrom-Json; Write-Host ('Result: '+$taskResult.status); if($taskResult.skills){Write-Host ('Skills: '+($taskResult.skills -join ', '))}; if($env:PM_ESSENTIAL_MODE -eq 'install'){Write-Host 'Installation complete. Use Codex normally when it next reloads its instructions. No project activation prompt is needed.'}; exit 0"
set "PM_ESSENTIAL_EXIT=%ERRORLEVEL%"
if "%PM_ESSENTIAL_PAUSE%"=="1" pause
exit /b %PM_ESSENTIAL_EXIT%
