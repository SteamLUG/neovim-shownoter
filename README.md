# [neovim-shownoter](https://github.com/SteamLUG/neovim-shownoter)

Copyright © 2016 Andrew "HER0" Conrad

**neovim-shownoter** is a Neovim plugin for editing SteamLUG Cast [shownotes](https://github.com/SteamLUG/steamlugcast-shownotes).

Functionality improves on the [web-based](https://steamlug.org/transcriberer)
editor, [Transcriberer](https://github.com/SteamLUG/transcriberer). Besides the
audio playback controls, neovim-shownoter's enhanced feature set includes:

* Always adding timestamps to the beginning of the line, instead of at the
cursor position. If a timestamp is already present, it is replaced.

* Seeking the audio to the timestamp on the current line.

* Automatic loading of local audio files.

* Support for customizing keybindings (see available [commands](#commands)). You
can even set the increments used for audio adjustments (skipping, changing
playback volume and speed).

All with the power of working in a vim-like editor!

neovim-shownoter is made available under the terms of the GNU GPL version 3. See
`COPYING` for details.

For more information on the `episode.txt` annotation files, see the
[description of the format/actual production source files](https://github.com/SteamLUG/steamlugcast-shownotes)
and their usage on the [Cast web pages](https://steamlug.org/cast).

## Requirements

* [Python 3.6](https://www.python.org)

* [python-vlc](https://github.com/oaubert/python-vlc)

* [Neovim python-client](https://github.com/neovim/python-client)

## Install

Quick install on Linux: Place `shownoter.py` in `~/.local/share/nvim/site/rplugin/python3`

Using remote plugins requires updating the remote plugin manifest. This can be
done with the Neovim command `:UpdateRemotePlugins`, which must be run after
install and after each update.

## Usage

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
| ShownoterFillBuffer          | Fills buffer with metadata and headings. WARNING: Do not use on a non-empty buffer | None |

On entering the buffer of a file named episode.txt, ShownoterSetAudio is run and
the key bindings are loaded. If the buffer is empty, ShownoterFillBuffer is run.
ShownoterInsertTimestamp and ShownoterSeekFromCurrentLine are unmapped on
leaving the buffer. The audio file, time, speed, and volume are remembered per
episode.txt buffer, for the duration of the session, and will swap back and
forth if editing multiple.

### Variables

Variables can be used to control certain settings.

| Variable                     | Description                                   |
| ---------------------------- | --------------------------------------------- |
| shownoter_no_mappings        | If true, no mappings are set                  |
| shownoter_no_insert_mappings | If true, mappings do not apply in insert mode |
| shownoter_audio_folder       | Path to folder containing Cast ogg files      |

## Contributing

If you have questions, a problem, or want to contribute code, please open an
issue report on [GitHub](https://github.com/SteamLUG/steamlugcast-shownotes/issues).
