import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from utils import compute_price

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
fig, ax = plt.subplots()
drink_names = list(st.session_state.drink_counter.keys())
drink_counts = compute_price(list(st.session_state.drink_counter.values()))
sns.barplot(x=drink_names, y=drink_counts, ax=ax)
ax.set_ylabel("Prezzo")
ax.set_title("Selezione dei Drink")
st.pyplot(fig)


st.table(table_data)
