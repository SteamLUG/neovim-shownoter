import neovim
import vlc
import datetime
import fnmatch
import os
import re

@neovim.plugin
class Shownoter(object):
	def __init__(self, nvim):
		self.nvim = nvim
		self.p = vlc.MediaPlayer('')
		self.buf_mem = {}
	
	@neovim.autocmd('BufEnter', pattern='episode.txt', sync=True)
	def load_info(self):
		buf = self.nvim.current.buffer.number
		if buf in self.buf_mem:
			if self.p is not self.buf_mem[buf]:
				self.pause_all()
				self.p = self.buf_mem[buf]
				self.show_echo('Audio file swapped')
			else:
				pass  # Already loaded
		else:
			self.set_audio()
		
		if self.nvim.current.buffer.get_line_slice(0, -1, True, True):
			self.fill_buffer()
		
		self.assign_keys()
	
	@neovim.autocmd('BufLeave', pattern='episode.txt', sync=True)
	def save_buf(self):
		buf = self.nvim.current.buffer.number
		self.buf_mem[buf] = self.p
		
		unmap_list = []
		if not self.nvim.vars.get('shownoter_no_mappings'):
			unmap_list.append('unmap <buffer> <M-p>')
			unmap_list.append('unmap <buffer> <M-CR>')
			if not self.nvim.vars.get('shownoter_no_insert_mappings'):
				unmap_list.append('unmap! <buffer> <M-p>')
				unmap_list.append('unmap! <buffer> <M-CR>')
		self.assign_keys(unmap_list)
	
	@neovim.command('ShownoterFillBuffer', sync=True)
	def fill_buffer(self):
		meta_lines = []
		meta_lines.append('RECORDED: ' + datetime.date.today().isoformat())
		meta_lines.append('PUBLISHED:')
		meta_lines.append('TITLE:')
		meta_lines.append('SEASON:')
		meta_lines.append('EPISODE:')
		meta_lines.append('DURATION:')
		meta_lines.append('FILENAME:')
		meta_lines.append('DESCRIPTION:')
		meta_lines.append('HOSTS:')
		meta_lines.append('GUESTS:')
		meta_lines.append('ADDITIONAL:')
		meta_lines.append('RATING:')
		meta_lines.append('YOUTUBE:')
		meta_lines.append('NOTESCREATOR:')
		meta_lines.append('EDITOR:')
		self.nvim.current.buffer.set_line_slice(0, 14, True, True, meta_lines)
		
		title_lines = []
		title_lines.append('*Introduction*')
		title_lines.append('*Our Gaming*')
		title_lines.append('*SteamLUG Community Stuff*')
		title_lines.append('*Steam/Valve News*')
		title_lines.append('*Tech News*')
		title_lines.append('*General Gaming News*')
		title_lines.append('*Crowdfunding*')
		title_lines.append('*Sign-off*')
		title_lines_with_spaces = []
		for l in range(8):
			title_lines_with_spaces.append("")
			title_lines_with_spaces.append(title_lines[l])
		self.nvim.current.buffer.set_line_slice(15, 31, True, True, title_lines_with_spaces)
	
	@neovim.command('ShownoterSetAudio', nargs='?', complete='file')
	def set_audio(self, filename=None):
		if filename is None:
			buf_path = os.path.split(os.path.abspath(self.nvim.current.buffer.name))
			for a_file in os.listdir(buf_path[0]):
				if fnmatch.fnmatch(a_file, '*.ogg'):
					filename = buf_path[0] + '/' + a_file
			if filename is None:
				self.show_echo('No audio found', warning=True)
				return
		elif not isinstance(filename, str):
			filename = str(filename).strip("[']")
		
		filename = os.path.abspath(filename)
		if os.path.exists(filename):
			self.p = vlc.MediaPlayer('file://' + filename)
			self.show_echo('Audio loaded: {}'.format(filename))
		else:
			self.show_echo('Audio file not found: {}'.format(filename), error=True)
	
	@neovim.command('ShownoterTogglePlay')
	def toggle_play(self):
		state = self.p.get_state().value
		time = self.p.get_time()
		length = self.p.get_length()
		
		if -1 < time < length:
			if state is vlc.State.Playing.value:
				self.p.pause()
				self.show_echo('Audio playback paused', message = False)
			elif state is vlc.State.Paused.value:
				self.p.play()
				self.show_echo('Audio playback resumed', message = False)
		else:
			self.p.stop()
			self.p.play()
			self.show_echo('Audio playback (re)started', message = False)
	
	@neovim.command('ShownoterPauseAll')
	def pause_all(self):
		self.p.pause()
		for player in self.buf_mem:
			if isinstance(player, vlc.MediaPlayer):
				player.pause()
	
	@neovim.command('ShownoterInsertTimestamp', sync=True)
	def insert_timestamp(self):
		timestamp = self.to_timestamp() + " "
		line = re.sub('^(\d{2}:?){3} ', '', self.nvim.current.line, 1)
		self.nvim.current.line = timestamp + line
	
	@neovim.command('ShownoterSeekFromCurrentLine')
	def seek_from_line(self):
		timestamp = re.match('^(\d{2}:?){3}', self.nvim.current.line)
		if timestamp:
			self.seek_timestamp(timestamp.group(0))
		else:
			self.show_echo('No timestamp on this line', error=True)
	
	@neovim.command('ShownoterSeekTimestamp', nargs='?')
	def seek_timestamp(self, timestamp='00:00:00'):
		self.p.set_position(self.to_msec(timestamp)/self.p.get_length())
		self.show_echo('Seeked to {}'.format(self.to_timestamp()))
	
	@neovim.command('ShownoterSkipTime', nargs='1')
	def skip(self, msecs):
		if not isinstance(msecs, int):
			msecs = int(str(msecs).strip("[']"))
		self.p.set_position((msecs + self.p.get_time())/self.p.get_length())
		self.show_echo('Skipped to {}'.format(self.to_timestamp()), message = False)
	
	@neovim.command('ShownoterChangeSpeed', nargs='?')
	def speed(self, c=0):
		if not isinstance(c, float):
			c = float(str(c).strip("[']"))
		if c is 0:
			c = 1
		else:
			c = c + self.p.get_rate()
		c = round(c, 4)
		self.p.set_rate(c)
		self.show_echo('Playback rate set to {}'.format(c), message = False)
	
	@neovim.command('ShownoterChangeVolume', nargs='?')
	def volume(self, c=0):
		if not isinstance(c, int):
			c = int(str(c).strip("[']"))
		if c is 0:
			c = 1
		else:
			c = c + self.p.audio_get_volume()
		self.p.audio_set_volume(c)
		self.show_echo('Playback volume set to {}'.format(c), message = False)
	
	@neovim.function('ShownotesToTimestamp')
	def to_timestamp(self, msecs=None):
		if not isinstance(msecs, int):
			try:
				msecs = int(str(msecs).strip("[']"))
			except:
				msecs = None
		if msecs is None:
			msecs = self.p.get_time()
		
		hours, msecs = divmod(msecs, 3600000)
		minutes, msecs = divmod(msecs, 60000)
		seconds, msecs = divmod(msecs, 1000)
		hms = [hours, minutes, seconds]
		for i in range(3):
			hms[i] = str(hms[i]).zfill(2)
		return(':'.join(hms))
	
	@neovim.function('ShownotesToMsec')
	def to_msec(self, timestamp):
		if not isinstance(timestamp, str):
			timestamp = str(timestamp).strip("[']")
		hms = timestamp.split(':')
		msecs = int(hms[0]) * 3600000
		msecs = int(hms[1]) * 60000 + msecs
		msecs = int(hms[2]) * 1000 + msecs
		return(msecs)
	
	def show_echo(self, text, message=True, warning=False, error=False):
		if message:
			command = 'echomsg "Shownoter: {}"'.format(text)
		else:
			command = 'echo "Shownoter: {}"'.format(text)
		if warning:
			command = 'echohl WarningMsg | {} | echohl None'.format(command)
		elif error:
			command = 'echohl ErrorMsg | {} | echohl None'.format(command)
		self.nvim.command(command)
	
	def assign_keys(self, map_list = []):
		if len(map_list) is not 0:
			for mapping in map_list:
				self.nvim.command(mapping)

		elif not self.nvim.vars.get('shownoter_no_mappings'):
			map_list.append('noremap <M-Space> :ShownoterTogglePlay<CR>')
			map_list.append('noremap <buffer> <M-p> :ShownoterInsertTimestamp<CR>')
			map_list.append('noremap <buffer> <M-CR> :ShownoterSeekFromCurrentLine<CR>')
			map_list.append('noremap <M-h> :ShownoterSkipTime -5000<CR>')
			map_list.append('noremap <M-H> :ShownoterSkipTime -10000<CR>')
			map_list.append('noremap <M-l> :ShownoterSkipTime 5000<CR>')
			map_list.append('noremap <M-L> :ShownoterSkipTime 10000<CR>')
			map_list.append('noremap <M-j> :ShownoterChangeSpeed -.10<CR>')
			map_list.append('noremap <M-k> :ShownoterChangeSpeed .10<CR>')
			map_list.append('noremap <M-J> :ShownoterChangeVolume -10<CR>')
			map_list.append('noremap <M-K> :ShownoterChangeVolume 10<CR>')
			
			if not self.nvim.vars.get('shownoter_no_insert_mappings'):
				map_list.append('noremap! <M-Space> <Esc>:ShownoterTogglePlay<CR>a')
				map_list.append('noremap! <buffer> <M-p> <Esc>:ShownoterInsertTimestamp<CR>a')
				map_list.append('noremap! <buffer> <M-CR> <Esc>:ShownoterSeekFromCurrentLine<CR>a')
				map_list.append('noremap! <M-h> <Esc>:ShownoterSkipTime -5000<CR>a')
				map_list.append('noremap! <M-H> <Esc>:ShownoterSkipTime -10000<CR>a')
				map_list.append('noremap! <M-l> <Esc>:ShownoterSkipTime 5000<CR>a')
				map_list.append('noremap! <M-L> <Esc>:ShownoterSkipTime 10000<CR>a')
				map_list.append('noremap! <M-j> <Esc>:ShownoterChangeSpeed -.10<CR>a')
				map_list.append('noremap! <M-k> <Esc>:ShownoterChangeSpeed .10<CR>a')
				map_list.append('noremap! <M-J> :ShownoterChangeVolume -10<CR>a')
				map_list.append('noremap! <M-K> :ShownoterChangeVolume 10<CR>a')
			
			for mapping in map_list:
				self.nvim.command(mapping)

