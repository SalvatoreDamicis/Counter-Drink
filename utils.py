from typing import List
import pandas as pd

LOWER_PRICE = 5
START_PRICE = 8


def compute_price(list_of_counts: List[int]):
    price_variation = (START_PRICE - LOWER_PRICE) * len(list_of_counts)
    sum_votes = sum(list_of_counts)
    if sum_votes == 0:
        return [START_PRICE] * len(list_of_counts)

    percentage = [count / sum_votes for count in list_of_counts]
    price = [LOWER_PRICE + round(p * price_variation) for p in percentage]

    return price


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


if __name__ == "__main__":
    # test_compute_price()
    simulation_party()

    # todo: make a casual simulator 
