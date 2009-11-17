/*
NSIS Minimum Required Lines of code (Commented out are recommended minimum lines of code)
@author: Sam Gleske
*/

; Uncomment this section for Vista/7 UAC access requirement. (none|user|highest|admin)
;RequestExecutionLevel user

; Best Compression, Uncomment the following four lines to achieve the best compression NSIS provides
;SetCompress auto
;SetCompressor /SOLID lzma
;SetCompressorDictSize 32
;SetDatablockOptimize on

OutFile "minimum.exe"

; Uncomment this section to make the installer run silent without user knowledge (normal|silent|silentlog)
;SilentInstall silent

;This is where your commands go.
Section "MainSection"
SectionEnd