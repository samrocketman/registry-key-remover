/*
RegShot Reverter NSIS Main File
@author: Sam Gleske
*/

; Script generated by the HM NIS Edit Script Wizard.

XPStyle on
CRCCheck on
RequestExecutionLevel user

; Best Compression
SetCompress Auto
SetCompressor /SOLID lzma
SetCompressorDictSize 32
SetDatablockOptimize On

; Includes
!include "regshot_reverter.nsh"
!include InstallOptions.nsh

; Global Variables
Var REGSHOT_TXT
Var NSIS_NSI

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "Registry Key Remover"
!define EXE_NAME "regshot_reverter.exe"
!ifndef PRODUCT_VERSION
  !define PRODUCT_VERSION "0.1.59"
!endif

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "..\dist\${EXE_NAME}"
LoadLanguageFile "${NSISDIR}\Contrib\Language files\English.nlf"
InstallDir "$TEMP\reverter\"
Icon "icon1.ico"
LicenseText "If you accept all the terms of the agreement, choose I Agree to continue. You must accept the agreement to run $(^Name)."
LicenseData "license.rtf"
BrandingText "Reverter for RegShot ${PRODUCT_VERSION}"
ShowInstDetails hide

VIProductVersion "${PRODUCT_VERSION}.0"
VIAddVersionKey /LANG=1033 "ProductName" "${PRODUCT_NAME} ${PRODUCT_VERSION}"
VIAddVersionKey /LANG=1033 "CompanyName" "${PRODUCT_NAME} Project"
VIAddVersionKey /LANG=1033 "LegalCopyright" "Copyright (C) 2009 ${PRODUCT_NAME} Project"
VIAddVersionKey /LANG=1033 "FileDescription" "Removes registry keys based on the snap shot provided by RegShot."
VIAddVersionKey /LANG=1033 "FileVersion" "${PRODUCT_VERSION}"
VIAddVersionKey /LANG=1033 "OriginalFilename" "${EXE_NAME}"

; Program Page Order
Caption "$(^Name)"
Page license
; Show custom dialog
Page custom AdvSettings ValidateSettings
Page instfiles

Function AdvSettings
; Display the InstallOptions dialog
  InstallOptions::initDialog /NOUNLOAD "$PLUGINSDIR\custom.ini"
; Now show the dialog and wait for it to finish
  InstallOptions::show
; Finally fetch the InstallOptions status value (we don't care what it is though)
  Pop $0
FunctionEnd

Function ValidateSettings
; Detect which elements are being clicked
!insertmacro WhichClick

; Alert the user that the mode is disabled.
  ReadINIStr $0 "$PLUGINSDIR\custom.ini" "Field 6" "State"
  StrCmp $0 "Revert Changes" +1 +3
  MessageBox MB_OK|MB_ICONEXCLAMATION "The Revert Changes option is currently not available.$\r$\nSorry for any inconvenience!"
  Abort

; Make sure the user references a real file for the RegShot snapshot txt file
  ReadINIStr $0 "$PLUGINSDIR\custom.ini" "Field 2" "State"
  IfFileExists $0 +3
  MessageBox MB_OK|MB_TOPMOST|MB_SETFOREGROUND|MB_ICONSTOP "RegShot text file does not exist!"
  Abort
  
; Path to the RegShot txt file
  StrCpy $REGSHOT_TXT $0

; Path to the NSIS File
  ReadINIStr $NSIS_NSI "$PLUGINSDIR\custom.ini" "Field 4" "State"
  IfFileExists $NSIS_NSI +1 +3
  MessageBox MB_YESNO|MB_ICONQUESTION|MB_SETFOREGROUND|MB_DEFBUTTON2 "NSIS File: $NSIS_NSI$\r$\nAlready exists! Do you wish to overwrite?" idYes +2
  Abort
FunctionEnd

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite on
  File "..\dist\python26.dll"
  File "..\dist\library.zip"
  File "..\dist\reverter.exe"
  Var /GLOBAL reverter
  StrCpy $reverter "$\"$INSTDIR\reverter.exe$\" -F $\"$REGSHOT_TXT$\" -N $\"$NSIS_NSI$\""
  ExecWait $reverter
  RmDir /r "$INSTDIR"
  DetailPrint ""
  DetailPrint "All done, Thanks for using Corey And Mike's Registry Reverter."
  DetailPrint "NSIS Script Generator written by Sam Gleske."
  DetailPrint "https://sourceforge.net/projects/registrykeyremo/"
SectionEnd

Function .onInit
; Check to ensure all required dependencies are met by the program
  IfFileExists "$SYSDIR\taskkill.exe" +2
    MessageBox MB_OK|MB_TOPMOST|MB_SETFOREGROUND|MB_ICONSTOP "Required Dependency Warning!\r\n$SYSDIR\taskkill.exe does not exist."
  IfFileExists "$SYSDIR\regsvr32.exe" +2
    MessageBox MB_OK|MB_TOPMOST|MB_SETFOREGROUND|MB_ICONSTOP "Required Dependency Warning!\r\n$SYSDIR\regsvr32.exe does not exist."
  IfFileExists "$SYSDIR\net.exe" +2
    MessageBox MB_OK|MB_TOPMOST|MB_SETFOREGROUND|MB_ICONSTOP "Required Dependency Warning!\r\n$SYSDIR\net.exe does not exist."
  IfFileExists "$SYSDIR\WSOCK32.dll" +2
    MessageBox MB_OK|MB_TOPMOST|MB_SETFOREGROUND|MB_ICONSTOP "Required Dependency Warning!\r\n$SYSDIR\WSOCK32.dll does not exist."
  IfFileExists "$SYSDIR\USER32.dll" +2
    MessageBox MB_OK|MB_TOPMOST|MB_SETFOREGROUND|MB_ICONSTOP "Required Dependency Warning!\r\n$SYSDIR\USER32.dll does not exist."
  IfFileExists "$SYSDIR\ADVAPI32.dll" +2
    MessageBox MB_OK|MB_TOPMOST|MB_SETFOREGROUND|MB_ICONSTOP "Required Dependency Warning!\r\n$SYSDIR\ADVAPI32.dll does not exist."
  IfFileExists "$SYSDIR\SHELL32.dll" +2
    MessageBox MB_OK|MB_TOPMOST|MB_SETFOREGROUND|MB_ICONSTOP "Required Dependency Warning!\r\n$SYSDIR\SHELL32.dll does not exist."
  IfFileExists "$SYSDIR\KERNEL32.dll" +2
    MessageBox MB_OK|MB_TOPMOST|MB_SETFOREGROUND|MB_ICONSTOP "Required Dependency Warning!\r\n$SYSDIR\taskkill.exe does not exist."


; Check if already running
; If so don't open another but bring to front
  System::Call "kernel32::CreateMutexA(i 0, i 0, t '$(^Name)') i .r0 ?e"
  Pop $0
  StrCmp $0 0 launch
   StrLen $0 "$(^Name)"
   IntOp $0 $0 + 1
  loop:
    FindWindow $1 '#32770' '' 0 $1
    IntCmp $1 0 +4
    System::Call "user32::GetWindowText(i r1, t .r2, i r0) i."
    StrCmp $2 "$(^Name)" 0 loop
    System::Call "user32::ShowWindow(i r1,i 9) i."         ; If minimized then maximize
    System::Call "user32::SetForegroundWindow(i r1) i."    ; Brint to front
    Abort
  launch:
  
; Plugins directory
  InitPluginsDir
  File /oname=$PLUGINSDIR\custom.ini "custom.ini"
  ; Automatically write the output path for the user's NSIS script starting out on the Desktop
  WriteINIStr "$PLUGINSDIR\custom.ini" "Field 4" "State" "$DESKTOP\auto_revert.nsi"
FunctionEnd