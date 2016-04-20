" Vim filetype plugin file
" Language: SteamLUG Cast shownotes file
" Maintainer: SteamLUG (https://steamlug.org)
" Last Change: 2016-04-20

if exists("b:did_ftplugin")
  finish
endif

au BufRead,BufNewFile episode.txt set filetype=castnote
