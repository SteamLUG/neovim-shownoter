import neovim
import vlc
import fnmatch
import os
import re

@neovim.plugin
class Shownoter(object):
	def __init__(self, nvim):
		self.nvim = nvim
		self.p = vlc.MediaPlayer('')
		self.buf_mem = {}
	
	@neovim.autocmd('BufEnter', pattern='episode.txt', sync=True) #, eval=':normal setlocal spell'
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
	
	@neovim.autocmd('BufLeave', pattern='episode.txt', sync=True)
	def save_buf(self):
		buf = self.nvim.current.buffer.number
		self.buf_mem[buf] = self.p
	
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
			
			#if self.p.will_play():  # Does not appear to act as expected...
			#	self.show_echo('Audio loaded: {}'.format(filename))
			#else:
			#	self.show_echo('Invalid audio format: {}'.format(filename), True)
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

