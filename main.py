from yahoo.balance_sheet_rows import DATE
from yahoo.ticker import MyTicker
from yahoo.timeframes import *
import numpy as np
import yfinance as ys
import matplotlib.pyplot as plt

plt.style.use("dark_background")


def main(startk: int, off: int):
    NFLX = MyTicker("NFLX")

    expected_prices = NFLX.get_results(startk, 38, off)
    expected_prices_s = NFLX.get_coefficients_result(
        NFLX.get_coefficients(startk, off), startk, 38
    )

    fig, ax = plt.subplots()
    ax.plot(
        NFLX.avg_price[DATE][1:],
        expected_prices,
        label="expected avg dynamic",
        color="red",
    )

    ax.plot(
        NFLX.avg_price[DATE],
        NFLX.avg_price[OPEN],
        label="actual avg",
        color="yellow",
    )

    ax.plot(
        NFLX.avg_price[DATE][1:],
        expected_prices_s,
        label="expected avg static",
        color="purple",
    )

    ax.plot(
        NFLX.price[DATE],
        NFLX.price[OPEN],
        label="actual price",
        color="green",
    )
    
    plt.axvline(
        x=NFLX.avg_price[DATE][off],
        color="white",
        linestyle="--",
        linewidth=2,
    )

    plt.legend()
    plt.show()

    # print(result, np.linalg.cond(result))


if __name__ == "__main__":
    main(0, 22)
