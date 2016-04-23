" Vim syntax file
" Language: SteamLUG Cast shownotes file
" Maintainer: SteamLUG (https://steamlug.org)
" Filenames: episode.txt
" Last Change: 2016-04-20

if exists("b:current_syntax")
  finish
endif

syn case match

syn region castnoteMetaData start=/\v%^/ end=/\v^$/ transparent contains=castnoteMetaDataLine
syn region castnoteMetaDataLine start=/\v^[A-Z]+:/ end=/$/ contained contains=castnoteMetaDataKey,castnoteTwitterHandle
syn match castnoteMetaDataKey /\v^[A-Z]+:/ contained

syn match castnoteTitle /\v\*(.)+\*/
syn match castnoteTimestamp /\v^(\d{2}:?){3}/

syn match castnotePreviousCast /\v\[s\d\de\d\d\]/
syn region castnoteCodeBlock start=/`/ end=/`/
syn match castnoteLink /\v<(https?|irc|steam):\/\/\S+>\/?/
syn match castnoteTwitterHandle /\v(\%^|^|\s|\()\zs\@[A-Za-z0-9_]+>/
syn match castnoteEmail /\v<[A-Za-z0-9._%+-]+\@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}>/

hi link castnoteMetaDataKey Define
hi link castnoteMetaDataLine Comment
hi link castnoteTitle Title
hi link castnoteTimestamp Number
hi link castnotePreviousCast Identifier
hi link castnoteCodeBlock String
hi link castnoteLink Underlined
hi link castnoteTwitterHandle Keyword
hi link castnoteEmail Type

let b:current_syntax = "castnote"

