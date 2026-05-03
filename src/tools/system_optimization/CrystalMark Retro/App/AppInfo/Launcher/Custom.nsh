${SegmentFile}

${SegmentInit}
	Rename "$EXEDIR\Data\CrystalMarkRetroConfig\CrystalMarkRetro64.ini" "$EXEDIR\Data\CrystalMarkRetroConfig\CrystalMarkRetro.ini"
	Rename "$EXEDIR\Data\CrystalMarkRetroConfig\CrystalMarkRetro32.ini" "$EXEDIR\Data\CrystalMarkRetroConfig\CrystalMarkRetro.ini"
	Rename "$EXEDIR\Data\CrystalMarkRetroConfig\CrystalMarkRetroA64.ini" "$EXEDIR\Data\CrystalMarkRetroConfig\CrystalMarkRetro.ini"
!macroend

${SegmentPre}
	ReadRegStr $0 HKLM "HARDWARE\DESCRIPTION\System" "Identifier"
	StrCpy $1 $0 3 0
		
	${If} $1 == "ARM"
		${ReadLauncherConfig} $ProgramExecutable Launch ProgramExecutableARM64
	${EndIf}
	
	${If} $Bits == "32"
		StrCpy $0 "32"
	${ElseIf} $1 == "ARM"
		StrCpy $0 "A64"
	${Else}
		StrCpy $0 "64"
	${EndIf}
	
	${If} ${FileExists} "$EXEDIR\Data\CrystalMarkRetroConfig\CrystalMarkRetro.ini"
		Rename "$EXEDIR\Data\CrystalMarkRetroConfig\CrystalMarkRetro.ini" "$EXEDIR\Data\CrystalMarkRetroConfig\CrystalMarkRetro$0.ini"
	${EndIf}
!macroend
