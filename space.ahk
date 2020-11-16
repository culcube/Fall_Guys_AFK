WinGet, current_ID, ID, A
WinActivate, FallGuys_client
sleep, 1
sendinput {space}
sleep, 1
WinActivate, ahk_id %current_ID%
return
exitapp
