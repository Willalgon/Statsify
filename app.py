import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# --- CONFIGURACIÓN SPOTIFY ---
CLIENT_ID = '809317ee17f24cfe97d00419dd824ff5'
CLIENT_SECRET = 'cebc2b43cff946358b874c1909203e45'
REDIRECT_URI = 'http://127.0.0.1:8888/callback'
SCOPE = 'user-top-read user-read-recently-played'

# --- AUTENTICACIÓN ---
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# --- STREAMLIT SETUP ---
st.set_page_config(page_title="🎧 Statsify", layout="wide")
st.title("🎧 Statsify - Tus datos musicales")
st.write("Explora tus estadísticas personales de Spotify.")

# --- SELECCIÓN DE TIEMPO ---
time_range_labels = {
    "Corto plazo (últimas 4 semanas)": "short_term",
    "Medio plazo (últimos 6 meses)": "medium_term",
    "Largo plazo (últimos años)": "long_term"
}
selected_label = st.selectbox("Selecciona el periodo de tiempo:", list(time_range_labels.keys()))
time_range = time_range_labels[selected_label]

# --- CANCIONES MÁS ESCUCHADAS ---
st.subheader("🎵 Tus 10 canciones favoritas")
top_tracks = sp.current_user_top_tracks(limit=10, time_range=time_range)

cols = st.columns(5)
for idx, track in enumerate(top_tracks['items']):
    col = cols[idx % 5]
    with col:
        st.image(track['album']['images'][0]['url'], width=150)
        st.caption(f"**{track['name']}**\n\n{track['artists'][0]['name']}")

# --- ARTISTAS MÁS ESCUCHADOS CON PORCENTAJES ---
st.subheader("🧑‍🎤 Tus 10 artistas favoritos y porcentaje relativo")

top_artists = sp.current_user_top_artists(limit=10, time_range=time_range)

# Sumamos popularidad para el cálculo porcentual aproximado
total_popularity = sum(artist['popularity'] for artist in top_artists['items'])

cols = st.columns(5)
for idx, artist in enumerate(top_artists['items']):
    col = cols[idx % 5]
    with col:
        st.image(artist['images'][0]['url'], width=150)
        porcentaje = (artist['popularity'] / total_popularity) * 100 if total_popularity > 0 else 0
        st.caption(f"**{artist['name']}**\n\n{porcentaje:.1f} % de tu escucha")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("💦 Hecho con ❤️ por guillee.ag 💦")
