import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from utils import compute_price
import base64
import time

# 001219, #005f73, #0a9396, #94d2bd, #e9d8a6, #ee9b00, #ca6702, #bb3e03, #ae2012, #9b2226
palette = ['#0081a7', '#00afb9', '#fdfcdc', "#fed9b7", "#f07167"]


def create_plot(drink_names, drink_counts, colors):
    # Creazione del grafico con valori sopra le barre
    fig, ax = plt.subplots()
    sns.barplot(x=drink_names, y=drink_counts, ax=ax, palette=colors)

    # Aggiungere il valore sopra ogni barra
    for index, value in enumerate(drink_counts):
        ax.text(index, value + 0.1, str(value) + ' €', ha='center', va='bottom')

    ax.set_title("Selezione dei Drink")
    ax.yaxis.set_visible(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    st.pyplot(fig)


def set_background(image_file):
    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()

    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)


set_background("background.jpg")
# Inserire il CSS nella pagina
st.title(" Liceo Counter Drink 🍹🍸🥃")

# Lista di drink
drink_list = ["Mojito", "Martini", "Negroni", "Old Fashioned", "Margarita"]
# Colori base e colore evidenziato
palette = ["#3498db"] * len(drink_list)  # Blu di default
highlight_color = "#e74c3c"  # Rosso per evidenziare

# Inizializza il conteggio dei drink nella sessione
if 'drink_counter' not in st.session_state:
    st.session_state.drink_counter = {drink: 0 for drink in drink_list}
if 'last_clicked' not in st.session_state:
    st.session_state.last_clicked = None


# Layout dei pulsanti
cols = st.columns(len(drink_list))
for col, drink in zip(cols, drink_list):
    if col.button(drink):
        st.session_state.drink_counter[drink] += 1
        st.session_state.last_clicked = drink  # Memorizza l'ultimo cliccato

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

# Effetto lampeggio: resetta il colore dopo 1 secondo
if st.session_state.last_clicked:
    time.sleep(1)
    st.session_state.last_clicked = None


