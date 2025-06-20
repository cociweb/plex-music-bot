from plexapi.exceptions import NotFound


class PlexMusic():
	def __init__(self, plex_library):
		self.library = plex_library
		self._total_track_count = None
		self._total_artist_count = None

	# Methods

	def recently_added_tracks(self, limit=50):
		return self.library_search('addedAt:desc', 'track', limit)

	def recently_played_tracks(self, limit=50):
		return self.library_search('lastViewedAt:desc', 'track', limit)

	def top_played_tracks(self, limit=50):
		return self.library_search('viewCount:desc', 'track', limit)

	def least_played_tracks(self, limit=50):
		return self.library_search('viewCount:asc', 'track', limit)

	def all_tracks(self):
		return self.library.all(libtype='track')

	def all_artists(self):
		return self.library.all(libtype='artist')

	def library_search(self, sort_value, media_type, limit):
		limit = int(limit)
		return self.library.search(sort=sort_value, libtype=media_type, limit=limit)

	def replace_playlist_tracks(self, playlist_title, playlist_songs):
		target_playlist = self.get_playlist(playlist_title)
		if not target_playlist:
			self.library.createPlaylist(playlist_title, items=playlist_songs)
		else:
			target_playlist.removeItems(target_playlist.items())
			target_playlist.addItems(playlist_songs)

	def get_playlist(self, playlist_title):
		try:
			return self.library.playlist(playlist_title)
		except NotFound:
			return None

	# Properties

	@property
	def total_track_count(self):
		if self._total_track_count is None:
			print('Retrieving total track count...')
			self._total_track_count = self.library.totalViewSize(libtype='track')
			print('Retrieving total track count... DONE.')
		return self._total_track_count

	@property
	def total_artist_count(self):
		if self._total_artist_count is None:
			print('Retrieving total artist count...')
			self._total_artist_count = self.library.totalViewSize(libtype='artist')
			print('Retrieving total artist count... DONE.')
		return self._total_artist_count
	
