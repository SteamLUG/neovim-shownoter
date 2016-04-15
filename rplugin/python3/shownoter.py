import neovim
import vlc
import fnmatch
import os

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
				self.nvim.command('echom "Shownoter: Audio file swapped"')
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
				self.nvim.command('echom "Shownoter: No audio found"')
				return
		elif not isinstance(filename, str):
			filename = str(filename).strip("[']")
		
		filename = os.path.abspath(filename)
		if os.path.exists(filename):
			self.p = vlc.MediaPlayer('file://' + filename)
			self.nvim.command('echom "Shownoter: Loaded {}"'.format(filename))
			
			#if self.p.will_play():  # Does not appear to act as expected...
			#	self.nvim.command('echom "Shownoter: Loaded {}"'.format(filename))
			#else:
			#	self.nvim.command('echom "Shownoter: {} not a valid format"'.format(filename))
		else:
			self.nvim.command('echom "Shownoter: Audio file not found {}"'.format(filename))
	
	@neovim.command('ShownoterTogglePlay')
	def toggle_play(self):
		if self.p.is_playing():
			self.p.pause()
			self.nvim.command('echom "Shownoter: Audio paused"')
		else:
			self.p.play()
			self.nvim.command('echom "Shownoter: Audio resumed"')
	
	@neovim.command('ShownoterPauseAll')
	def pause_all(self):
		for player in self.buf_mem:
			player.pause()
	
	@neovim.command('ShownoterInsertTimestamp', sync=True)
	def insert_timestamp(self):
		timestamp = self.to_timestamp()
		self.nvim.current.line = timestamp + self.nvim.current.line
	
	@neovim.command('ShownoterSeekFromCurrentLine')
	def seek_from_line(self):
		timestamp = self.nvim.current.line.split(maxsplit=1)[0]
		self.seek_timestamp(timestamp)
	
	@neovim.command('ShownoterSeekTimestamp', nargs='?')
	def seek_timestamp(self, timestamp='00:00:00'):
		self.p.set_time(self.to_msec(timestamp))
		self.nvim.command('echom "Shownoter: Seeked to {}"'.format(to_timestamp()))
	
	@neovim.command('ShownoterSkipTime', nargs='1')
	def skip(self, msecs):
		self.p.set_time(msecs + self.p.get_time())
		self.nvim.command('echom "Shownoter: Skipped to {}"'.format(to_timestamp()))
	
	@neovim.command('ShownoterChangeSpeed', nargs='?')
	def speed(self, c=0):
		if c is 0:
			c = 1
		else:
			c = c + self.p.get_rate()
		self.p.set_rate(c)
		self.nvim.command('echom "Shownoter: Playback rate set to {}"'.format(c))
	
	@neovim.command('ShownoterChangeVolume', nargs='?')
	def volume(self, c=0):
		if c is 0:
			c = 1
		else:
			c = c + self.p.audio_get_volume()
		self.p.audio_set_volume(c)
		self.nvim.command('echom "Shownoter: Playback volume set to {}"'.format(c))
	
	@neovim.function('ShownotesToTimestamp')
	def to_timestamp(self, msecs=None):
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
		hms = timestamp.split(':')
		msecs = int(hms[0]) * 3600000
		msecs = int(hms[1]) * 60000 + msecs
		msecs = int(hms[2]) * 1000 + msecs
		return(msec)

