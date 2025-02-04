import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from utils import compute_price
#001219, #005f73, #0a9396, #94d2bd, #e9d8a6, #ee9b00, #ca6702, #bb3e03, #ae2012, #9b2226
palette = ['#0081a7', '#00afb9', '#fdfcdc', "#fed9b7", "#f07167"]

st.title(" Liceo Counter Drink")
st.write("Benvenuto al Liceo Counter Drink! 🍹🍸🥃")
st.write("Bevi un drink per aumentare il prezzo:")

# Lista di drink
drink_list = ["Mojito", "Martini", "Negroni", "Old Fashioned", "Margarita"]

# Inizializza lo stato della sessione per il conteggio se non esiste
if 'drink_counter' not in st.session_state:
    st.session_state.drink_counter = {drink: 0 for drink in drink_list}


# Creazione dei pulsanti per ogni drink
cols = st.columns(len(drink_list))
for col, drink in zip(cols, drink_list):
    if col.button(drink):
        st.session_state.drink_counter[drink] += 1

# Mostra il conteggio attuale
table_data = [[drink, count] for drink, count in st.session_state.drink_counter.items()]

# Mostra il grafico a barre
drink_names = list(st.session_state.drink_counter.keys())
drink_counts = compute_price(list(st.session_state.drink_counter.values()))

# Creazione del grafico con valori sopra le barre
fig, ax = plt.subplots()
sns.barplot(x=drink_names, y=drink_counts, ax=ax, palette=palette)

# Aggiungere il valore sopra ogni barra
for index, value in enumerate(drink_counts):
    ax.text(index, value + 0.1, str(value) + ' €', ha='center', va='bottom')

ax.set_title("Selezione dei Drink")
ax.yaxis.set_visible(False)

for spine in ax.spines.values():
    spine.set_visible(False)

st.pyplot(fig)
