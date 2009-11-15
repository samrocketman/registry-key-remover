echo off
cls
REM Compile Executable using a batch file
REM @author: Sam Gleske

REM Here are the things you need to compile this successfully:
REM 	Python 2.6 (latest)
REM 	py2exe for Python 2.6 (latest)
REM 	7-Zip command line utilitiy (make sure 7za.exe is in the same directory as this batch file!)
REM Additional notes:
REM 	You may need to add your python directory (where python.exe is located) to your PATH environment variable.


:: No matter where the batch file is run, run it as if being run from the same dir as RunPython2EXE.bat
%~d0
cd %~dp0

:: Compile extra modules
python compile.py

:: Compile exe file and library files
python setup.py py2exe

:: Add compiled modules (pyc) to the library.zip archive to be used by the EXE (exclude all CVS directories and *.py source files)
set zip=%~dp07za.exe
set zipfile=%~dp0dist\library.zip
cd src\Reverter
dir /s /b | find /i ".pyc" | "%zip%" a -xr!*CVS* -xr!*.py "%zipfile%" 

:: Remove all compiled modules from source directories
echo Removing all compiled modules from source directories
del /q /s *.pyc
:: Remove unnecessary files from binary dist directory
echo Removing unnecessary files from dist directory.
cd %~dp0dist
del /q *.pyd
del /q w9xpopen.exe
echo.
echo.
echo.
echo.
echo "All done! __init__.exe should be located in the dist/ directory"
pause