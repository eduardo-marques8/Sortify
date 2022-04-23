from distutils.log import error
class Track:
    def __init__(self, _name, _artist, _popularity, _releaseDate):
        self.name = _name
        self.artist = _artist
        # self.language = _language
        # self.listeningFrequency = _listeningFrequency
        self.popularity = _popularity
        self.releaseDate = _releaseDate

class Playlist:
    def __init__(self, _tracks):
        self.tracks = _tracks

    def addTrack(self, _track):
        self.tracks.append(_track)
    
    def printTracksDetail(self):
        for track, i in zip(self.tracks, range(len(self.tracks))):
            print(f"Track #{i} -> '{track.name}' from '{track.artist}'")
            try:
                print(f'     --> Popularity: {track.popularity}')
                print(f'     --> Release date: {track.releaseDate}')
            except error:
                print(error)

    def printTracksOrder(self):
        for track, i in zip(self.tracks, range(len(self.tracks))):
            print(f'#{i}: {track.name}')