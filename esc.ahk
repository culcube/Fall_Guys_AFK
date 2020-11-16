WinGet, current_ID, ID, A
WinActivate, FallGuys_client
sleep, 1
sendinput {Esc}
sleep, 1
WinActivate, ahk_id %current_ID%
return
exitapp
