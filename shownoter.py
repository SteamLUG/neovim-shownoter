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
	
	@neovim.autocmd('BufEnter', pattern='episode.txt', eval='set spell', sync=True)
	def load_info(self):
		buf = self.nvim.current.buffer.number
		if buf in self.buf_mem:
			if self.p is not buf_mem[buf]:
				self.pause_all()
				self.p = buf_mem[buf]
			else:
				pass  # Already loaded
		else:
			self.set_audio()
	
	@neovim.autocmd('BufLeave', pattern='episode.txt', sync=True)
	def save_buf(self):
		buf = self.nvim.current.buffer.number
		self.buf_mem[buf] = self.p
	
	@neovim.command('ShownoterSetAudio', nargs='?')
	def set_audio(self, filename):
		if filename is None:
			buf_path = os.path.split(os.path.abspath(self.nvim.current.buffer.name))
			for file in os.listdir(buf_path[0]):
				if fnmatch.fnmatch(file, '*.ogg'):
					filename = buf_path[0] + file
		else:
			filename = os.path.abspath(filename)
		
		if os.path.exists(filename):
			self.p = vlc.MediaPlayer('file://' + filename)
			self.nvim.command('echom "Loaded {}"'.format(filename))
			
			#if self.p.will_play():  # Does not appear to act as expected...
			#	self.nvim.command('echom "Loaded {}"'.format(filename))
			#else:
			#	self.nvim.command('echom "{} not a valid format"'.format(filename))
		else:
			self.nvim.command('echom "Audio file not found"')
	
	@neovim.command('ShownoterTogglePlay')
	def toggle_play(self):
		if self.p.is_playing():
			self.p.pause()
			self.nvim.command('echom "Audio paused"')
		else:
			self.p.play()
			self.nvim.command('echom "Audio resumed"')
	
	@neovim.command('ShownoterPauseAll')
	def pause_all(self):
		for m in self.p:
			m.pause()
	
	@neovim.command('ShownoterInsertTimestamp', sync=True)
	def insert_timestamp(self):
		timestamp = self.to_timestamp(self.p.get_time())
		pass
	
	@neovim.command('ShownoterSeekTimestamp', nargs='?')
	def seek_timestamp(self, timestamp='00:00:00'):
		self.p.set_time(self.to_msec(timestamp))
		pass
	
	@neovim.command('ShownoterSkipTime', nargs='1')
	def skip(self, msecs):
		self.p.set_time(msecs + self.p.get_time())
	
	@neovim.command('ShownoterChangeSpeed', nargs='?')
	def speed(self, c=0):
		if c is 0:
			c = 1
		else:
			c = c + self.p.get_rate()
		self.p.set_rate(c)
		self.nvim.command('echom "Playback rate set to {}"'.format(c))
	
	@neovim.command('ShownoterChangeVolume', nargs='?')
	def volume(self, c=0):
		if c is 0:
			c = 1
		else:
			c = c + self.p.audio_get_volume()
		self.p.audio_set_volume(c)
		self.nvim.command('echom "Playback volume set to {}"'.format(c))
	
	@neovim.function('ShownotesToTimestamp')
	def to_timestamp(self, msecs):
		hours, msecs = divmod(msecs, 3600000)
		minutes, msecs = divmod(msecs, 60000)
		seconds, msecs = divmod(msecs, 1000)
		hms = [hours, minutes, seconds]
		for i in range(3):
			hms[i] = str(hms[i]).rjust(2, '0')
		return(':'.join(hms))
	
	@neovim.function('ShownotesToMsec')
	def to_msec(self, timestamp):
		hms = timestamp.split(':')
		msecs = int(hms[0]) * 3600000
		msecs = int(hms[1]) * 60000 + msecs
		msecs = int(hms[2]) * 1000 + msecs
		return(msec)

