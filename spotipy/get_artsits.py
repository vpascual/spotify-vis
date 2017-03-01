import spotipy
import spotipy.util as util
import simplejson as json
import time

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

    for i, t in enumerate(features):
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

if __name__ == '__main__':
    #artists = ['Radiohead', 'Muse', 'Biffy Clyro', 'Moderat', 'Placebo', 'CHVRCHES', 'Coldplay', 'Standstill', 'Apparat', 'Vetusta Morla']
    artists = ["!!! (Chk Chk Chk)", "7 Notas 7 Colores", "Abdulla Rashim", "About Leaving", "The Afghan Whigs", "Against Me!", "Agorazein", "Alex Cameron", "Alexandra Savior", "Alien Tango", "Âme live", "Angel Olsen", "Anímic", "Annette Peacock", "Aphex Twin", "Arcade Fire", "Aries", "Aurora Halal", "Autarkic", "Avalon Emerson", "BADBADNOTGOOD", "Barbott", "Belako", "Ben UFO", "Berri Txarrak", "Bicep", "The Black Angels", "Bon Iver", "Broken Social Scene", "Cigarettes After Sex", "CLUBZ", "Dj Coco", "Conttra", "Converge", "Cymbals Eat Guitars", "The Damned", "Dave P.", "Death Grips", "Descendents", "Discos Paradiso Crew", "Dixon", "Don't DJ", "Dj Dustin", "El Petit de Cal Eril", "Elmini", "Elza Soares", "Fatima Yamaha", "Ferenc", "Flying Lotus", "Formation", "Frank Ocean", "Front 242", "Gas", "Glass Animals", "Gojira", "Gordi", "Grace Jones", "Grandaddy", "The Growlers", "Hamilton Leithauser", "Henrik Schwarz", "Her Little Donkey", "Huerco S.", "HVOB", "InnerCut", "Iosonouncane", "It's Not Not", "Japandroids", "Jardín de la Croix", "Jeremy Jay", "JMII", "Joey Purp", "John Talabot Disco Set", "Joy Orbison", "Julia Jacklin", "Julie Doiron", "Junun featuring Shye Ben Tzur & The Rajasthan Express", "Kate Tempest", "Kelly Lee Owens", "Kepa Junkera & Los Hermanos Cubero", "Kevin Morby", "Khidja", "King Gizzard & The Lizard Wizard", "King Krule", "King Sunny Adé", "KiNK", "Kokoshca", "Kornél Kovács", "Lady Wray", "Lauer", "Les Cruet", "Les Sueques", "Let's Eat Grandma", "Local Natives", "Lord Of The Isles", "Lvl Up", "Mac DeMarco", "The Magnetic Fields", "The Make-Up", "Mannequin Pussy", "Màquina Total", "Marc Piñol", "Maresme", "Marie Davidson", "Marta Delmont", "Matrixxman", "Medalla", "Melange", "Metronomy", "Michael Mayer", "Miguel", "Mishima", "Mitski", "The Molochs", "Moscoman live band", "Muñeco", "Murdoc", "Museless", "The Mystery Lights", "Nikki Lane", "No Zu", "Noga Erez", "Nots", "Ocellot", "Odina", "Operators", "PAVVLA", "Pearson Sound", "Pedro Vian", "Pender Street Steppers", "Phurpa", "Pinegrove", "Playback Maracas", "Polar Inertia", "Pond", "Preoccupations", "Priests", "Rebuig", "Recondite", "Retirada!", "Romare", "Rosalía & Raül Refree", "Royal Trux", "Run The Jewels", "S U R V I V E", "Saint Etienne", "Salfumán", "Sampha", "Sau Poler", "Seu Jorge plays The Life Aquatic. A Tribute to David Bowie", "Shelby Grey", "Shellac", "Sinkane", "Skepta", "Skinny Puppy", "Slayer", "Sleaford Mods", "Sleep", "Slim Cessna's Auto Club", "Solange", "Soledad Vélez", "Sorry Kate", "Swans", "Swet Shop Boys", "Talaboman", "Teenage Fanclub", "Dj Tennis", "This Is Not This Heat", "Triángulo de Amor Bizarro", "Tuff City Kids", "Tycho", "Vaadat Charigim", "Van Morrison", "Vladimir Ivkovic", "Vox Low", "Wand", "The Waterparties", "The Wave Pictures", "The Wedding Present", "Weval", "Weyes Blood", "The Wheels", "Whitney", "Wild Beasts", "William Tyler", "The xx", "Youandewan", "Young Marco", "The Zombies perform Odessey & Oracle 50th Anniversary"]

    features = []

    for artist in artists:
        tracks = []
        result = get_artist(artist)
        print(result)
        #print(result['uri'])
        #top_tracks = sp.artist_top_tracks(result['uri'])
        #print(top_tracks)
        #tids  = [o['uri'] for o in top_tracks['tracks']]
        #print(tracks_ids)

        albums_ids = get_artist_albums(result['uri'])

        for album in albums_ids:
            tracks += get_album_tracks(album)

        artist_features = get_features(tracks)

        for f in artist_features:
            f['band'] = artist

        features += artist_features

    str = json.dumps(features)

    text_file = open("bands_spotipy.json", "w")
    text_file.write(str)
    text_file.close()
    #for track in features['tracks']:
    #    print(track)
