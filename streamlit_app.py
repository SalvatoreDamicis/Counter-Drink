import streamlit as st
from utils import compute_price, create_plot, set_background_video, START_PRICE, drink_list
import time
from PIL import Image

TIMER_DURATION = 20  # 5 minuti = 300 secondi

palette = ["#e0e1dd"] * len(drink_list)  # Blu di default
highlight_color = "#e74c3c"  # Rosso per evidenziare

# Inizializza il conteggio dei drink nella sessione
if 'drink_counter' not in st.session_state:
    st.session_state.drink_counter = {drink: START_PRICE for drink in drink_list}
if 'last_clicked' not in st.session_state:
    st.session_state.last_clicked = None
if 'highlight_end' not in st.session_state:
    st.session_state.highlight_end = 0
if 'drink_history' not in st.session_state:
    st.session_state.drink_history = []  # Lista per lo storico
if "show_image" not in st.session_state:
    st.session_state.show_image = False
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

st.set_page_config(layout="wide")
set_background_video()
col1, col2 = st.columns([15, 1])

with col2:
    # Bottone per resettare e mostrare/nascondere l'immagine
    if st.button(" "):
        st.session_state.show_image = not st.session_state.show_image  # Alterna la visibilità dell'immagine

if st.session_state.show_image:
    img = Image.open("crollo_borsa.jpg")
    st.image(img, use_container_width=True)

# 🔥 Creiamo margini laterali per restringere il contenuto
left_margin, main_content, right_margin = st.columns([0.2, 2.6, 0.2])

# 📌 Espande lo spazio centrale con CSS
custom_css = """
    <style>
        section.main.block-container {
            max-width: 1800px !important;  /* Cambia a piacere (1200px, 1600px, etc.) */
            padding-left: 5rem !important;
            padding-right: 5rem !important;
        }
        [data-testid="stSidebar"] {
            background-color: black !important;
        }
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        .stButton > button {
            width: 120%;
            font-size: 1.2rem;
            padding: 10px;
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

with main_content:
    st.columns([0.3, 0.5, 0.2])[1].title(":green[Stocks Drinks 🍹]")
    # Layout dei pulsanti
    num_cols = 5
    rows = [drink_list[i:i + num_cols] for i in range(0, len(drink_list), num_cols)]  # 2 righe

    for row in rows:
        cols = st.columns([0.8, 0.2, 0.8, 0.2, 0.8, 0.2, 0.8, 0.2, 0.8, 0.15])  # Alterna spazio e pulsante

        drink_index = 0  # Tiene traccia dei drink posizionati
        for i, col in enumerate(cols):
            if i % 2 == 0:  # Solo le colonne dispari contengono pulsanti
                with col:
                    if drink_index < len(row):  # Evita errori se ci sono meno drink
                        if st.button(row[drink_index], use_container_width=True):
                            # st.session_state.drink_counter[row[drink_index]] += 1
                            st.session_state.last_clicked = row[drink_index]
                            st.session_state.highlight_end = time.time() + 1
                            st.session_state.drink_history.append(row[drink_index])
                        drink_index += 1

    # Assegna i colori: cambia solo quello selezionato
    current_palette = palette.copy()
    if st.session_state.last_clicked:
        idx = drink_list.index(st.session_state.last_clicked)
        current_palette[idx] = highlight_color

    # Mostra il conteggio attuale
    table_data = [[drink, count] for drink, count in st.session_state.drink_counter.items()]

    # Mostra il grafico a barre
    drink_names = list(st.session_state.drink_counter.keys())
    st.session_state.drink_counter = compute_price(st.session_state.drink_counter,
                                                   st.session_state.last_clicked)

    drink_counts = list(st.session_state.drink_counter.values())
    create_plot(drink_names, drink_counts, current_palette)

    # Ricarica la pagina dopo 1 secondo per rimuovere il colore evidenziato
    if time.time() >= st.session_state.highlight_end:
        st.session_state.last_clicked = None
    st.session_state.highlight_end = 0

    # 📌 Storico dei drink sulla destra
with st.sidebar:
    st.subheader("📝 Sold Drinks")
    if st.session_state.drink_history:
        for drink in reversed(st.session_state.drink_history[-20:]):  # Mostra solo gli ultimi 10
            st.write(f"🍹 {drink}")
    else:
        st.write("None")
