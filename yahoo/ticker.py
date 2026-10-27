from datetime import date, timedelta
from enum import Enum
import yfinance as yf
from pathlib import Path
import numpy as np
from yahoo.constants import TimeFrames, Candle, Tikers
from .balance_sheet_rows import DATE


def to_yf_date(_date: date) -> str:
    return _date.strftime("%Y-%m-%d")


def from_bloomberg_str_date(_date: str) -> date:
    mm, gg, yy = map(int, _date.split("/"))
    return date(yy, mm, gg)


def from_yahoo_str_date(_date: str) -> date:
    yy, mm, gg = map(int, _date.split("-"))
    return date(yy, mm, gg)


def get_date_avg(date1: date, date2: date):
    assert date1 < date2
    return date1 + (date2 - date1) // 2




class MyTicker:
    def __init__(self, ticker: str):
        self.ticker = ticker

        self.__financials = None

        self.__price = None
        self.__avg_price = None

    @property
    def start_date(self):
        return self.financials[0][DATE]

    @property
    def end_date(self):
        return self.financials[-1][DATE]

    @property
    def price(self):
        if not self.price_path.exists():
            self.download_ticker_data(
                start=self.start_date,
                end=self.end_date + timedelta(days=90),
                interval=TimeFrames.D1,
            )

        if self.__price is None:
            with open(self.price_path) as f:
                self.__price = [[], []]
                for line in f.readlines()[3:]:
                    date, price = line.split(",")[: Candle.O + 1]
                    self.__price[0].append(from_yahoo_str_date(date))
                    self.__price[1].append(price)

                self.__price = [
                    np.array(self.__price[0], dtype="datetime64[D]"),
                    np.array(self.__price[1], dtype="float"),
                ]

        return self.__price

    @property
    def financials(self) -> np.ndarray:
        if self.__financials is None:
            with open(self.financials_path) as f:
                file_data = []
                for row in f.readlines()[1:]:
                    date, *data = row.replace(",", ".").split(";")
                    file_data.append(
                        [from_bloomberg_str_date(date), *map(float, data)]
                    )
            self.__financials = np.array(file_data)
        return self.__financials

    @property
    def avg_price(self):
        if self.__avg_price is None:
            self.__avg_price = self.get_avg_price()

        return self.__avg_price

    def get_avg_price(self):
        financials = self.financials

        price_index = 0
        avg = [[], []]

        for date in financials[1:, DATE]:
            _sum = 0
            _len = 0

            start_date = self.price[DATE][price_index]
            
            while date > self.price[DATE][price_index]:
                _sum += float(self.price[Candle.O][price_index])
                price_index += 1
                _len += 1

            avg[0].append(get_date_avg(start_date, date))
            avg[1].append(_sum / _len)

        return [
            np.array(avg[0], dtype="datetime64[D]"),
            np.array(avg[1], dtype="float"),
        ]

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

        if price is not None:
            price.to_csv(self.price_path)
        # financials.to_csv(dist_path / 'financials2.csv')

    def get_coeff_matrix(self, start: int, end: int):
        # self.avg_price[start:end] are the prices before the balance sheet
        # where P0 = self.avg_price[start:end], P1 = self.avg_price[start + 1:end + 1]
        # (P0; financials)(coeffs) = P1

        return np.hstack(
            [
                np.ones((end - start, 1)),
                self.avg_price[Candle.O][start:end].reshape(-1, 1),
                self.financials[start:end, 1:].astype(float),
            ]
        )

    def get_coefficients(self, start: int, end: int) -> np.ndarray:
        # first price is the price before the first financial data
        # the price to be predicted starts 1 after
        avg_price = self.avg_price[Candle.O][start + 1 : end + 1].reshape(-1, 1)
        coeffs = np.linalg.pinv(self.get_coeff_matrix(start, end)) @ avg_price

        return coeffs

    def get_coefficients_result(self, coeffs, start: int, end: int): 
        return self.get_coeff_matrix(start, end) @ coeffs

    def get_results(self, start: int, end: int, off=20):
        # training
        coefficients = self.get_coefficients(start, off)
        result = list(
            self.get_coeff_matrix(start, off) @ coefficients
        )

        for i in range(off, end):
            result.append(self.get_coeff_matrix(0, end)[i] @ coefficients)
            coefficients = self.get_coefficients(start, i + 1)

        return result, self.get_corr(result, off, end)

    def get_corr(self, result, start, end):

        y = self.avg_price[1][start + 1:end + 1]
        y_hat = np.array([result_i[0] for result_i in result[start:end]])

        avg_y = np.mean(y)

        s_y = np.sum((y - avg_y) ** 2)
        s_error = np.sum((y - y_hat) ** 2)

        return 1 - s_error / s_y


