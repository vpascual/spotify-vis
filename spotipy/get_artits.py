import spotipy
import spotipy.util as util
import simplejson as json
import time
import os

scope = 'user-top-read'
token = util.prompt_for_user_token('victor.pascual', scope)
sp = spotipy.Spotify(auth=token)
sp.trace = False

def get_artist(name):
    print("Searching for " + name)
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

def get_features(tracks):
    track_ids = [o['uri'] for o in tracks]
    chunks = [track_ids[x:x + 50] for x in range(0, len(track_ids), 50)]
    features = []
    for chunk in chunks:
        features += sp.audio_features(chunk) # maximum of 50 tracks
        # time.sleep(30)

    for i, t in enumerate(features):
        if t is not None:
            t['name'] = tracks[i]['name']
            t['album'] = tracks[i]['album']

    return features

def get_artist_albums(artist_id):
    albums = sp.artist_albums(artist_id, album_type='album', country=None, limit=20, offset=0)
    #albums_ids = [o['uri'] for o in albums['items']]
    #print(albums_ids)
    return albums['items']

def get_album_tracks(album):
    album_id = album['uri']
    tracks = sp.album_tracks(album_id, limit=50, offset=0)
    #track_ids = [o['uri'] for o in tracks['items']]
    #print(track_ids)

    items = tracks['items']
    for item in items:
        item['album'] = album['name']
        del item['available_markets']

    return tracks['items']

def get_tracks_from_festival(festival, artists):

    #artists = artists_madcool

    features = []
    bands = []

    for artist in artists:
        tracks = []
        attempts = 0
        while True:
            try:
                result = get_artist(artist)
                # time.sleep(20)
                print(result)
            except Exception:
                attempts = attempts + 1
                time.sleep(10)

                if attempts > 20:
                    break
                else:
                    continue
            break


        #print(result['uri'])
        #top_tracks = sp.artist_top_tracks(result['uri'])
        #print(top_tracks)
        #tids  = [o['uri'] for o in top_tracks['tracks']]
        #print(tracks_ids)

        if result is None:
            continue

        bands.append(result)

        albums_ids = get_artist_albums(result['uri'])

        for album in albums_ids:
            # time.sleep(50)
            tracks += get_album_tracks(album)

        artist_features = get_features(tracks)

        for f in artist_features:
            if f is not None:
                f['band'] = artist

        features += artist_features


    str = json.dumps(features)

    text_file = open(festival + "_spotipy.json", "w")
    text_file.write(str)
    text_file.close()

    str = json.dumps(bands)
    text_file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bands_data",  "bands_" + festival + "_spotipy.json"), "w")
    text_file.write(str)
    text_file.close()


def get_bands_from_festival(festival, artists):

    bands = []

    for artist in artists:
        tracks = []
        attempts = 0
        while True:
            try:
                result = get_artist(artist)
                # time.sleep(20)
                print(result)
            except Exception:
                attempts = attempts + 1
                time.sleep(10)

                if attempts > 20:
                    break
                else:
                    continue
            break


        #print(result['uri'])
        #top_tracks = sp.artist_top_tracks(result['uri'])
        #print(top_tracks)
        #tids  = [o['uri'] for o in top_tracks['tracks']]
        #print(tracks_ids)

        if result is None:
            continue

        bands.append(result)


    str = json.dumps(bands)

    text_file = open("bands_" + festival + "_spotipy.json", "w")
    text_file.write(str)
    text_file.close()
    #for track in features['tracks']:
    #    print(track)
