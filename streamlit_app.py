import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from utils import compute_price, set_background, create_plot
import base64
import time

# 001219, #005f73, #0a9396, #94d2bd, #e9d8a6, #ee9b00, #ca6702, #bb3e03, #ae2012, #9b2226
# palette = ['#0081a7', '#00afb9', '#fdfcdc', "#fed9b7", "#f07167"]

drink_list = ["Mojito", "Martini", "Negroni", "Old Fashioned",
              "Margarita", "Daiquiri", "Whiskey Sour", "Cosmopolitan",
              "Pina Colada", "Manhattan"]

st.set_page_config(layout="wide")
# 🔥 Creiamo margini laterali per restringere il contenuto
left_margin, main_content, right_margin = st.columns([0.2, 2.6, 0.2])

set_background("background.jpg")
# Inserire il CSS nella pagina

# Lista di drink
# Colori base e colore evidenziato
palette = ["#3498db"] * len(drink_list)  # Blu di default
highlight_color = "#e74c3c"  # Rosso per evidenziare

# Inizializza il conteggio dei drink nella sessione
if 'drink_counter' not in st.session_state:
    st.session_state.drink_counter = {drink: 0 for drink in drink_list}
if 'last_clicked' not in st.session_state:
    st.session_state.last_clicked = None
if 'highlight_end' not in st.session_state:
    st.session_state.highlight_end = 0
if 'drink_history' not in st.session_state:
    st.session_state.drink_history = []  # Lista per lo storico

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
    st.columns([0.3, 0.5, 0.2])[1].title(" Liceo Counter Drink 🍹🍸🥃")
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
                            st.session_state.drink_counter[row[drink_index]] += 1
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
    drink_counts = compute_price(list(st.session_state.drink_counter.values()))

    create_plot(drink_names, drink_counts, current_palette)

    # Ricarica la pagina dopo 1 secondo per rimuovere il colore evidenziato
    if time.time() >= st.session_state.highlight_end:
        st.session_state.last_clicked = None
        st.session_state.highlight_end = 0

# 📌 Storico dei drink sulla destra
with st.sidebar:
    st.subheader("📝 Storico Drink Presi")
    if st.session_state.drink_history:
        for drink in reversed(st.session_state.drink_history[-20:]):  # Mostra solo gli ultimi 10
            st.write(f"🍹 {drink}")
    else:
        st.write("Nessun drink selezionato.")
