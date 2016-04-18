# neovim-shownoter

Neovim plugin for editing SteamLUG Cast [shownotes](https://github.com/SteamLUG/steamlugcast-shownotes)

Github project page available at https://github.com/SteamLUG/neovim-shownoter

## Requirements

* Python 3

* python-vlc

* Neovim python-client

## Install

Quick install on Linux: Place `shownoter.py` in `~/local/share/nvim/site/rplugin/python3`

Using remote plugins requires updating the remote plugin manifest. This can be done with the neovim command `:UpdateRemotePlugins`, which must be run after install and after each update.

## Usage

This plugin is intended specifically to help with editing the episode.txt files used for SteamLUG Cast shownotes. See [description of the format/actual production source files](https://github.com/SteamLUG/steamlugcast-shownotes) and [their usage on the Cast web pages](https://steamlug.org/cast). Functionality is based on [Transcriberer](https://github.com/SteamLUG/transcriberer).

### Commands

| Command                      | Description                                         | Mapping       |
| ---------------------------- | --------------------------------------------------- | ------------- |
| ShownoterSetAudio            | Loads audio path or guesses from current dir        | None          |
| ShownoterTogglePlay          | Toggles audio playback                              | Alt + Space   |
| ShownoterPauseAll            | Pauses all playback (should never be needed)        | None          |
| ShownoterInsertTimestamp     | Adds/replaces leading timestamp with current        | Alt + p       |
| ShownoterSeekFromCurrentLine | Seeks audio to timestamp at beginning of line       | Alt + Enter   |
| ShownoterSeekTimestamp       | Seeks audio to provided timestamp (in hh:mm:ss)     | None          |
| ShownoterSkipTime            | Skips forward/back by provided milliseconds         | Forward 5sec: Alt + l, Back 5sec: Alt + h, Forward 10sec: Alt + L, Back 10sec: Alt + H |
| ShownoterChangeSpeed         | Shifts playback speed up/down by decimal, or resets | Up .10: Alt + k, Down .10: Alt + j |
| ShownoterChangeVolume        | Increases/decreases volume by int, or resets        | Up 10: Alt + K, Down 10: Alt + J  |

On entering the buffer of a file named episode.txt, ShownoterSetAudio is run and the key bindings are loaded. ShownoterInsertTimestamp and ShownoterSeekFromCurrentLine are unmapped on leaving the buffer. The audio file, time, speed, and volume are remembered are remembered per episode.txt, and will swap back and forth if editing multiple.

### Variables

Variables can be used to control certain settings.

| Variable                     | Description                                   |
| ---------------------------- | --------------------------------------------- |
| shownoter_no_mappings        | If true, no mappings are set                  |
| shownoter_no_insert_mappings | If true, mappings do not apply in insert mode |
