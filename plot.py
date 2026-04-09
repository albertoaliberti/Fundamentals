from yahoo.balance_sheet_rows import DATE
from yahoo.ticker import MyTicker
import matplotlib.pyplot as plt
from yahoo.timeframes import *

def plot(startk: int, off: int, ticker: str):
    tk = MyTicker(ticker)

    expected_prices = tk.get_results(startk, 38, off)
    expected_prices_s = tk.get_coefficients_result(
        tk.get_coefficients(startk, off), startk, 38
    )

    _, ax = plt.subplots()
    
    ax.plot(
        tk.avg_price[DATE][1:],
        expected_prices,
        label="expected avg dynamic",
        color="red",
    )

    ax.plot(
        tk.avg_price[DATE],
        tk.avg_price[OPEN],
        label="actual avg",
        color="yellow",
    )

    ax.plot(
        tk.avg_price[DATE][1:],
        expected_prices_s,
        label="expected avg static",
        color="purple",
    )

    ax.plot(
        tk.price[DATE],
        tk.price[OPEN],
        label="actual price",
        color="green",
    )
    
    plt.axvline(
        x=tk.avg_price[DATE][off],
        color="white",
        linestyle="--",
        linewidth=2,
    )

    plt.legend()
    plt.show()