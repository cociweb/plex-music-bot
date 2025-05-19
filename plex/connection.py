from plexapi.myplex import MyPlexAccount

class PlexConnection():
	def __init__(self, username=None, password=None, resource=None, section_name="Music"):
		self.username = username
		self.password = password
		self.resource = resource
		self._server = None
		self._section_name = section_name

	@property
	def music_library(self):
		return self.library.section(self._section_name)

	@property
	def library(self):
		return self.server.library

	@property
	def server(self):
		if not self._server:
			self._server = self._setup_server()
		return self._server

	def _setup_server(self):
		print(f'Connecting to Plex server {self.resource}...')
		account = MyPlexAccount(self.username, self.password)
		print(f'Connecting to Plex server {self.resource}... DONE.')
		return account.resource(self.resource).connect()
