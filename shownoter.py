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
			self.p = buf_mem[buf]
		else:
			self.set_audio()
	
	@neovim.autocmd('BufLeave', pattern='episode.txt', sync=True)
	def save_buf(self):
		buf = self.nvim.current.buffer.number
		self.buf_mem[buf] = self.p
	
	@neovim.function('SetAudio')
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
	
	@neovim.function('TogglePlay')
	def toggle_play(self):
		if self.p.is_playing():
			self.nvim.command('echom "Pausing"')
			self.p.pause()
		else:
			self.nvim.command('echom "Playing"')
			self.p.play()
	
	@neovim.function('InsertTimestamp')
	def insert_timestamp(self):
		self.p.get_time()
		pass
	
	@neovim.function('SeekTimestamp')
	def seek_timestamp(self, args):
		self.p.set_time()
		pass
	
	@neovim.function('Skip')
	def skip(self):
		self.p.get_time()
		self.p.set_time()
		pass
	
	@neovim.function('Speed')
	def speed(self, args):
		self.p.get_rate()
		self.p.set_rate()
		pass
	
	@neovim.function('Volume')
	def volume(self, args):
		self.p.audio_get_volume()
		self.p.audio_set_volume()
		pass

