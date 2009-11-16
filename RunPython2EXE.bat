echo off
title Sam's Autobuilding batch file
cls
REM Compile Executable using a batch file
REM @author: Sam Gleske

REM Here are the things you need to compile this successfully:
REM 	Python 2.6 (latest)
REM 	py2exe for Python 2.6 (latest)
REM 	7-Zip command line utilitiy (make sure 7za.exe is extracted in the same directory as this batch file!)
REM 	NSIS 2.45
REM Additional notes:
REM 	You will need to add entries to your PATH environment variable (these are examples, not the same on all systems):
REM 		C:\python26\ (Python 2.6 directory where python.exe is located)
REM 		C:\Program Files\NSIS\ (NSIS 2.45 directory where makensis.exe is located)


:: No matter where the batch file is run, run it as if being run from the same dir as RunPython2EXE.bat
%~d0
cd %~dp0

:: Version of software: MAJOR.MINOR.PATCHSET
set VERSION=0.1.58

:: Ask pesky version questions so you don't forget to update them
echo Current MAJOR.MINOR.PATCHSET=%VERSION%
echo Did you update the version number in the following files:
set /p MessageUser="  RunPython2EXE.bat (0.1.PATCHSET) (y/n)?: "
if /I "%MessageUser%" neq "y" Goto End
set /p MessageUser="  NSIS\regshot_reverter.nsi (0.1.PATCHSET) (y/n)?: "
if /I "%MessageUser%" neq "y" Goto End
set /p MessageUser="  Setup.py (0.1.PATCHSET) (y/n)?: "
if /I "%MessageUser%" neq "y" Goto End

:: Compile extra modules
python compile.py

:: Compile exe file and library files
python setup.py py2exe

:: Add compiled modules (pyc) to the library.zip archive to be used by the EXE (exclude all CVS directories and *.py source files)
set zip=%~dp07za.exe
set zipfile=%~dp0dist\library.zip
cd src\Reverter
dir /s /b | find /i ".pyc" | "%zip%" a -tzip -xr!*CVS* -xr!*.py "%zipfile%" 

:: Remove all compiled modules from source directories
echo Removing all compiled modules from source directories
del /q /s *.pyc
:: Remove unnecessary files from binary dist directory
echo Removing unnecessary files from dist directory.
cd %~dp0dist
del /q *.pyd
del /q w9xpopen.exe

:: Put together the binaries
copy __init__.exe reverter.exe
del __init__.exe
makensis /DPRODUCT_VERSION="%VERSION%" "..\NSIS\regshot_reverter.nsi"
copy /y ..\README.txt .\
copy /y ..\NSIS\license.rtf .\

:: Prepare binary packages for upload to sourceforge
mkdir ..\packages
del ..\packages\regshot_reverter_i386*
dir /s /b | "%zip%" a -tzip -xr!*CVS* ..\packages\regshot_reverter_i386_v%VERSION%.zip
cd ..
dir /s /b | "%zip%" a -tzip -xr!*CVS* -xr!*dist* -xr!*build* -xr!*packages* -xr!*.exe packages\regshot_reverter_i386_v%VERSION%_src.zip
cls
echo Build Complete if you had your environment set up correctly.
echo.
echo There should be 2 packages in the packages/ directory:
echo   regshot_reverter_i386_v%VERSION%.zip
echo   regshot_reverter_i386_v%VERSION%_src.zip
pause
:End