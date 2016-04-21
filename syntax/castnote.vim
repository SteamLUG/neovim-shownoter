" Vim syntax file
" Language: SteamLUG Cast shownotes file
" Maintainer: SteamLUG (https://steamlug.org)
" Filenames: episode.txt
" Last Change: 2016-04-20

if exists("b:current_syntax")
  finish
endif

syn case match

syn match castnoteMetaDataKey /\m^[A-Z]\+:/
"syn match castnoteMetaDataValue /\m^[A-Z]\+:\s\zs.*$/

syn match castnoteTitle /\m*\(.\)\+\*/
syn match castnoteTimestamp /\m^\(\d\{2}:\?\)\{3}/

syn match castnotePreviousCast /\m\[s\d\de\d\d]/
syn region castnoteCodeBlock start=/`/ end=/`/
syn match castnoteHTTP /\mhttps\?:\/\/\(\S\)\+\ze[, \n]/
syn match castnoteTwitterHandle /\m@\(\S\)\+\ze[, \n]/

hi link castnoteMetaDataKey Define
hi link castnoteMetaDataValue Comment
hi link castnoteTitle Title
hi link castnoteTimestamp Number
hi link castnotePreviousCast Identifier
hi link castnoteCodeBlock String
hi link castnoteHTTP Underlined
hi link castnoteTwitterHandle Keyword

let b:current_syntax = "castnote"

