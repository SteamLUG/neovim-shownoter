" Vim filetype plugin file
" Language: SteamLUG Cast shownotes file
"           https://github.com/SteamLUG/steamlugcast-shownotes
" Maintainer: Andrew Conrad <aconrad103@gmail.com>
" Last Change: 2017-06-21

if exists("b:did_ftplugin")
  finish
endif

au BufRead,BufNewFile episode.txt set filetype=castnote
