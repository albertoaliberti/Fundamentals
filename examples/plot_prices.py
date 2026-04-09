import matplotlib.pyplot as plt
import tickers
from plot import plot

plt.style.use("dark_background")

if __name__ == "__main__":
    plot(0, 22, tickers.AAPL)
