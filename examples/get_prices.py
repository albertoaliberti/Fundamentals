from yahoo.balance_sheet_rows import DATE
from yahoo.ticker import MyTicker
import matplotlib.pyplot as plt
from yahoo.timeframes import *
import tickers

tk = MyTicker(tickers.NFLX)
startk = 0
off = 20

# weights calculated with the matrix with prices from startk to startk + off 
# one weigths are calculated, they remain the same for the subsequent data 
expected_prices = tk.get_results(startk, 38, off)

# weights calculated with the matrix with prices from startk to startk + off
# once the startk + off price is calculated, at the next iteration, 
# the weights are recalculated with a matrix that includes also the previous prices
expected_prices_s = tk.get_coefficients_result(
        tk.get_coefficients(startk, off), startk, 38
)