import streamlit as st
from streamlit_oauth import OAuth2Component
import spotipy

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="🎧 Statsify", layout="wide")
st.title("🎧 Statsify - Tus datos musicales")
st.write("Explora tus estadísticas personales de Spotify.")

# --- CLIENTE OAUTH ---
client_id = st.secrets["SPOTIPY_CLIENT_ID"]
client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
redirect_uri = "https://<tu_usuario>.streamlit.app"  # Sustituye <tu_usuario>

oauth2 = OAuth2Component(
    client_id=client_id,
    client_secret=client_secret,
    authorize_endpoint="https://accounts.spotify.com/authorize",
    token_endpoint="https://accounts.spotify.com/api/token",
    redirect_uri=redirect_uri,
    scopes=["user-top-read", "user-read-recently-played"],
)

token = oauth2.authorize_button("Inicia sesión con Spotify", "spotify")

if token:
    sp = spotipy.Spotify(auth=token["access_token"])

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
    total_popularity = sum(artist['popularity'] for artist in top_artists['items'])

    cols = st.columns(5)
    for idx, artist in enumerate(top_artists['items']):
        col = cols[idx % 5]
        with col:
            st.image(artist['images'][0]['url'], width=150)
            porcentaje = (artist['popularity'] / total_popularity) * 100 if total_popularity > 0 else 0
            st.caption(f"**{artist['name']}**\n\n{porcentaje:.1f} % de tu escucha")

    st.markdown("---")
    st.caption("💦 Hecho con ❤️ por guillee.ag 💦")

else:
    st.warning("Por favor inicia sesión con tu cuenta de Spotify.")
