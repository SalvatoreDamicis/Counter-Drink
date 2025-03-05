from typing import List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import base64
import random
drink_list = ["Spritz Aperol", "Spritz Campari", "Negroni", "Americano",
              "Gin Tonic", "Gin Lemon", "Vodka Lemon", "Paloma",
              "Cynar Fizz", "Moscow Mule"]
START_PRICE = 8
LOWER_PRICE = {drink: 5 for drink in drink_list}
LOWER_PRICE["Spritz Aperol"] = 4
LOWER_PRICE["Spritz Campari"] = 4
UPPER_PRICE = {drink: 12 for drink in drink_list}
UPPER_PRICE["Spritz Aperol"] = 8
UPPER_PRICE["Spritz Campari"] = 8


def set_background():
    image_file = 'background.jpg'
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


def set_background_video():
    # 🔥 Link diretto al video (sostituiscilo con il tuo)
    gif_path = 'stonks.gif'
    with open(gif_path, "rb") as gif_file:
        gif_base64 = base64.b64encode(gif_file.read()).decode()

    # HTML + CSS per impostare la GIF come sfondo
    background_html = f"""
        <style>
            .stApp {{
                background: url("data:image/gif;base64,{gif_base64}") no-repeat center center fixed;
                background-size: cover;
            }}
        </style>
        """

    st.markdown(background_html, unsafe_allow_html=True)


def create_plot(drink_names, drink_counts, colors):
    # Creazione del grafico con valori sopra le barre
    fig, ax = plt.subplots(figsize=(16, 7))
    sns.barplot(x=drink_names, y=drink_counts, ax=ax, palette=colors)

    # Aggiungere il valore sopra ogni barra
    for index, value in enumerate(drink_counts):
        ax.text(index, value + 0.1, str(value) + ' €', ha='center', va='bottom')

    ax.set_title("Selezione dei Drink")
    ax.yaxis.set_visible(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    st.pyplot(fig)


def compute_price(dict_of_counts: dict, select_drink: str):
    dict_of_counts_copy = dict_of_counts.copy()
    for drink, price in dict_of_counts_copy.items():
        if drink == select_drink:
            dict_of_counts[drink] = price + 1
            if dict_of_counts[drink] > UPPER_PRICE[drink]:
                dict_of_counts[drink] = UPPER_PRICE[drink]
            if dict_of_counts[drink] < LOWER_PRICE[drink]:
                dict_of_counts[drink] = LOWER_PRICE[drink]
    if select_drink:
        drink_to_choose = [drink for drink in dict_of_counts.keys() if drink != select_drink]
        random_drinks = random.sample(drink_to_choose, 2)
        for drink in random_drinks:
            dict_of_counts[drink] = dict_of_counts[drink] - 1
            if dict_of_counts[drink] > UPPER_PRICE[drink]:
                dict_of_counts[drink] = UPPER_PRICE[drink]
            if dict_of_counts[drink] < LOWER_PRICE[drink]:
                dict_of_counts[drink] = LOWER_PRICE[drink]

    return dict_of_counts


def test_compute_price():
    assert compute_price([0, 0, 0, 0, 0]) == [6, 6, 6, 6, 6]
    assert compute_price([1, 1, 1, 1, 1]) == [6, 6, 6, 6, 6]
    assert compute_price([0, 0, 0, 0, 5]) == [3, 3, 3, 3, 18]
    assert compute_price([1, 1, 1, 2, 5]) == [5, 5, 5, 6, 11]
    assert compute_price([0, 0, 0, 5, 5]) == [3, 3, 3, 8, 8]


def simulation_party():
    drink_list = ["Mojito", "Martini", "Negroni", "Old Fashioned", "Margarita"]
    drink_counter = {drink: 0 for drink in drink_list}
    price_time_party = {}
    for i in range(300):
        price_time_party[i] = compute_price(list(drink_counter.values()))
        low_cost_drink = min(drink_counter, key=drink_counter.get)
        drink_counter[low_cost_drink] += 1

    sim = pd.DataFrame.from_dict(price_time_party, orient='index', columns=drink_list)
    sim['buy'] = sim.min(axis=1)
    sim.to_csv('simulation_party.csv')
    print(sum(sim['buy']))


# Funzione per mostrare/nascondere il pop-up

if __name__ == "__main__":
    # test_compute_price()
    simulation_party()

    # todo: make a casual simulator
