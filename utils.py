from typing import List

LOWER_PRICE = 3
START_PRICE = 6


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
    assert compute_price([1, 1, 1, 2, 5]) == [5, 5, 5, 6, 8]
    assert compute_price([0, 0, 0, 5, 5]) == [3, 3, 3, 8, 8]


if __name__ == "__main__":
    test_compute_price()
