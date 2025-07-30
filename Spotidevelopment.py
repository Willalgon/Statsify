import spotipy
from spotipy.oauth2 import SpotifyOAuth # SpotifyOAuth es la clase que gestiona la autenticación OAuth 2.0, necesaria para acceder a datos privados de un usuario (como sus canciones favoritas).

CLIENT_ID = '809317ee17f24cfe97d00419dd824ff5'
CLIENT_SECRET = 'cebc2b43cff946358b874c1909203e45'
REDIRECT_URI = 'http://127.0.0.1:8888/callback'


SCOPE = 'user-top-read user-read-recently-played'
sp = spotipy.Spotify(auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# Canciones más escuhadas:
top_tracks = sp.current_user_top_tracks(limit=10, time_range='short_term')
print("\n🎵 Tus 10 cacniones más escuchadas este mes:\n")
for i, track in enumerate(top_tracks['items']):
    nombre = track['name']
    artista = track['artists'][0]['name']
    print(f"{i+1}. {nombre} - {artista}")

# Artistas más escuchados
top_artists = sp.current_user_top_artists(limit=10, time_range='short_term')
print("\🧑‍🎤 Tus 10 artistas más escuchados este mes: \n")
for i, artist in enumerate(top_artists['items']):
    print(f"{i+1}. {artist['name']}")