/*
RegShot Reverter NSIS Header File
@author: Sam Gleske
*/

!macro WhichClick
; The WhichClick macro is based off of a provided example in the InstallOptions examples
; of the NSIS installation.  Based off of testnotify.nsi

; At this point the user has either pressed Next or one of our custom buttons
; We find out which by reading from the INI file
  ReadINIStr $0 "$PLUGINSDIR\custom.ini" "Settings" "State"
  StrCmp $0 0  validate  ; Next button clicked?
  Abort
  validate:
!macroend