from datetime import date, timedelta
import yfinance as yf
from pathlib import Path
import numpy as np

from yahoo.timeframes import D1, OPEN
from .balance_sheet_rows import DATE


def to_yf_date(_date: date) -> str:
    return _date.strftime("%Y-%m-%d")


def from_bloomberg_str_date(_date: date) -> date:
    mm, gg, yy = map(int, _date.split("/"))
    return date(yy, mm, gg)


def from_yahoo_str_date(_date: date) -> date:
    yy, mm, gg = map(int, _date.split("-"))
    return date(yy, mm, gg)


def get_perc_delta(a, b):
    return a / b


class MyTicker:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.__financials = None
        self.__avg_price = None

    @property
    def financials(self):
        if self.__financials is None:
            with open(self.financials_path) as f:
                self.__financials = []
                for row in f.readlines()[1:]:
                    date, *data = row.replace(",", ".").split(";")
                    self.__financials.append(
                        [from_bloomberg_str_date(date), *map(float, data)]
                    )
            self.__financials = np.array(self.__financials)
        return self.__financials

    @property
    def avg_price(self):
        if not self.price_path.exists():
            financials = self.financials
            self.download_ticker_data(
                start=financials[0][DATE],
                end=financials[-1][DATE] + timedelta(days=90),
                interval=D1,
            )

        if self.__avg_price is None:
            with open(self.price_path) as f:
                self.__avg_price = self.get_avg_price(f.readlines())
            self.__avg_price = np.array(self.avg_price)

        return self.__avg_price

    def get_avg_price(self, lines: list[str]):
        financials = self.financials

        price_index = 3
        avg = []

        for date in financials[1:, DATE]:
            _sum = 0
            _len = 0

            parse_line = lambda: lines[price_index].split(",")
            l = parse_line()
            while date > from_yahoo_str_date(l[0]):
                _sum += float(l[OPEN])
                price_index += 1
                _len += 1
                l = parse_line()
            avg.append(_sum / _len)

        return avg

    @property
    def path(self):
        return Path(f"data/{self.ticker}")

    @property
    def price_path(self) -> Path:
        return self.path / "price.csv"

    @property
    def financials_path(self) -> Path:
        return self.path / "financials.csv"

    def download_ticker_data(self, start: date, end: date, interval: str):
        price = yf.download(self.ticker, start=start, end=end, interval=interval)
        # financials = yf.Ticker(self.ticker).get_financials(freq='quarterly')

        if not self.path.exists():
            self.path.mkdir()

        price.to_csv(self.price_path)
        # financials.to_csv(dist_path / 'financials2.csv')

    def get_coeff_matrix(self, start: int, end: int):
        return get_perc_delta(
            self.financials[start:end, 1:].astype(float),
            self.financials[start - 1 : end - 1, 1:].astype(float),
        )

    def get_coefficients(self, start: int, end: int) -> np.ndarray:
        coeff_matrix = self.get_coeff_matrix(start, end)
        avg_price = get_perc_delta(
            self.avg_price[start:end],
            self.avg_price[start - 1 : end - 1],
        )
        coeffs = np.linalg.pinv(coeff_matrix) @ avg_price.reshape(-1, 1)

        return coeffs

    def get_coefficients_results(self, coefficients: np.ndarray, start: int, end: int):
        return (
            self.get_coeff_matrix(start, end) @ coefficients,
            get_perc_delta(self.avg_price[start:end], self.avg_price[start - 1 : end - 1]),
            self.financials[start:end, DATE].astype("datetime64[D]"),
        )
