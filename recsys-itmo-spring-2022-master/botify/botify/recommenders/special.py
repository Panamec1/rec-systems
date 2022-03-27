import random
from typing import List


from .recommender import Recommender
from .random import Random


class Special(Recommender):
    def __init__(self, tracks_redis, artists_redis, catalog, top_singers):
        self.tracks_redis = tracks_redis
        self.artists_redis = artists_redis
        self.catalog = catalog

        self.random = Random(tracks_redis)
        #self.top_singers = top_singers
        self.top_tracks = top_singers

    def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:

        
        if self.top_tracks and (prev_track_time < 0.4):
            shuffled = list(self.top_tracks)
            random.shuffle(shuffled)
            return shuffled[0]
            #shuffled = list(self.top_singers)
            #random.shuffle(shuffled)
            #artist_data = self.artists_redis.get( shuffled[0])

            #if artist_data is not None:
            #    artist_tracks = self.catalog.from_bytes(artist_data)
            #else:
            #    return self.random.recommend_next(user, prev_track, prev_track_time)
            #index = random.randint(0, len(artist_tracks) - 1)
            #return artist_tracks[index]


        track_data = self.tracks_redis.get(prev_track)
        if track_data is not None:
            track = self.catalog.from_bytes(track_data)
        else:
            raise ValueError(f"Track not found: {prev_track}")

        artist_data = self.artists_redis.get(track.artist)
        if artist_data is not None:
            artist_tracks = self.catalog.from_bytes(artist_data)
        else:
            return self.random.recommend_next(user, prev_track, prev_track_time)

        index = random.randint(0, len(artist_tracks) - 1)
        return artist_tracks[index]
