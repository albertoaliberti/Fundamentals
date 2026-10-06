from yahoo.balance_sheet_rows import DATE
from yahoo.ticker import MyTicker, Tikers
import matplotlib.pyplot as plt
from yahoo.constants import *


def plot(startk: int, off: int, ticker: str, legend_fontsize=None):
    tk = MyTicker(ticker)

    expected_prices, coeff = tk.get_results(startk, 38, off)
    expected_prices_s = tk.get_coefficients_result(
        tk.get_coefficients(startk, off), startk, 38
    )

    print(coeff)

    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title(ticker)  # type: ignore

    ax.plot(
        tk.avg_price[DATE][1:],
        expected_prices,
        label="expected avg dynamic",
        color="red",
    )

    ax.plot(
        tk.avg_price[DATE],
        tk.avg_price[Candle.O],
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
        tk.price[Candle.O],
        label="actual price",
        color="green",
    )

    plt.axvline(
        x=tk.avg_price[DATE][off],
        color="white",
        label="end of training period",
        linestyle="--",
        linewidth=2,
    )

    plt.legend(fontsize=legend_fontsize)
    plt.show()

plt.style.use("dark_background")

if __name__ == "__main__":
    plot(0, 22, Tikers.AAPL)