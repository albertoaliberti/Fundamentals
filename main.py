from yahoo.balance_sheet_rows import DATE
from yahoo.ticker import MyTicker
from yahoo.timeframes import *
import numpy as np
import matplotlib.pyplot as plt


def main(startk: int, endk: int):
    NFLX = MyTicker("NFLX")
    coeffs = NFLX.get_coefficients(startk, endk)

    expected_prices, actual_prices, dates = NFLX.get_coefficients_results(
        coeffs, startk, 38
    )

    fig, ax = plt.subplots()
    ax.plot(dates, expected_prices, label="expected")

    ax.plot(dates, actual_prices, label="actual")
    plt.axvline(x=dates[endk], color="red", linestyle="--", linewidth=2)

    plt.legend()
    plt.show()

    # print(result, np.linalg.cond(result))


if __name__ == "__main__":
    main(1, 25)
