from yahoo.balance_sheet_rows import DATE
from yahoo.ticker import MyTicker
from yahoo.timeframes import *
import numpy as np
import matplotlib.pyplot as plt

def bars(x, y, labels, off=0.2):
    pos = np.arange(len(x))
    
    for i in range(len(y)):
        plt.bar(pos + i * off, y[i], off, label=labels[i])
   
    plt.xticks(pos + (len(y) - 1) * off / 2, x, rotation=45, ha='right')  # centramento e rotazione
    plt.legend()
    plt.tight_layout()  # evita che le etichette escano fuori dal grafico
    plt.show()



def main(startk: int, endk: int):
    NFLX = MyTicker("NFLX")
    coeffs = NFLX.get_coefficients(startk, endk)

    expected_prices, actual_prices, dates = NFLX.get_coefficients_results(
        coeffs, startk, 37
    )

    err = np.linalg.norm(expected_prices - actual_prices) / np.linalg.norm(actual_prices)

    print(err)

    fig, ax = plt.subplots()

    bars(dates, [expected_prices.ravel(), actual_prices], labels=["expected", "actual"])
    plt.axvline(x=endk, color="red", linestyle="--", linewidth=2)


    plt.legend()
    plt.show()

    # print(result, np.linalg.cond(result))


if __name__ == "__main__":
    main(1, 20)
