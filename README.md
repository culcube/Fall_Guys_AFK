# Fall_Guys_AFK

A python script to automate the joining of Fall Guys games, including leaving the show when knocked out after the first round.

NOTE: These scripts do not perform any in-game actions, apart from occasionally jumping, and so will not help you cheat to win any shows. In other words this is not a bot in any meaningful sense, and is not set up to allow users to cheat.

Requirements:

Windows

Fall Guys:    https://store.steampowered.com/app/1097150/Fall_Guys_Ultimate_Knockout/

python:       https://www.python.org/downloads/windows/

imagesearch:  https://brokencode.io/how-to-easily-image-search-with-python/

these files:  https://github.com/culcube/Fall_Guys_AFK


Set your starting exp in a file called: fg_xp

If you do not do this it will assume your starting xp is 0 - chnages are logged and the xp is only used to stop the afk script once you hit 40,000, i.e. level 40

run it in a terminal:
  python ./fall_guys_afk.py

output files are:

log: a copy of the timestamped entries for the checks (which are also sent to stdout) - useful for debugging if the script isn't working. If this happens consider increasing the number for that check in sub_loops

xp.csv: a comma separated variable file that records datetime and xp whenever this is logged

fg_xp: the current xp that you have, or the total xp the bot has gained if it wasn't initially set
