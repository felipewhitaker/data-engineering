from abc import ABC, abstractmethod

import requests
import logging

from datetime import datetime

import ratelimit
from backoff import on_exception, expo

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Currency(ABC):

    BASE_URL = "https://www.mercadobitcoin.net/api/"
    CURRENCIES = {
        "AAVE",
        "ACMFT",
        "ACORDO01",
        "ASRFT",
        "ATMFT",
        "AXS",
        "BAL",
        "BARFT",
        "BAT",
        "BCH",
        "BTC",
        "CAIFT",
        "CHZ",
        "COMP",
        "CRV",
        "DAI",
        "DAL",
        "ENJ",
        "ETH",
        "GALFT",
        "GRT",
        "IMOB01",
        "IMOB02",
        "JUVFT",
        "KNC",
        "LINK",
        "LTC",
        "MANA",
        "MBCONS01",
        "MBCONS02",
        "MBFP01",
        "MBFP02",
        "MBFP03",
        "MBFP04",
        "MBFP05",
        "MBPRK01",
        "MBPRK02",
        "MBPRK03",
        "MBPRK04",
        "MBPRK05",
        "MBVASCO01",
        "MCO2",
        "MKR",
        "OGFT",
        "PAXG",
        "PSGFT",
        "REI",
        "REN",
        "SNX",
        "UMA",
        "UNI",
        "USDC",
        "WBX",
        "XRP",
        "YFI",
        "ZRX",
    }

    def __init__(self, currency: str):
        self._currency = currency
        return

    @property
    def currency(self) -> str:
        return self._currency

    @currency.setter
    def _set_currency(self, currency: str):
        assert currency in self.CURRENCIES
        self._currency = currency

    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=25, period=30)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=20)
    def get_data(self, /, *args, **kwargs) -> dict:
        url = self._get_endpoint(*args, **kwargs)
        logger.info(f" Getting data from {url}")
        req = requests.get(self.BASE_URL + url)
        req.raise_for_status()
        return req.json()

    @abstractmethod
    def _get_endpoint(self, /, **kwargs) -> dict:
        pass


class DaySummaryAPI(Currency):

    PATH = "day-summary"

    def _get_endpoint(self, date: datetime) -> dict:
        year, month, day = date.year, date.month, date.day
        url = f"{self.currency}/{self.PATH}/{year}/{month}/{day}/"
        return url


class TradeAPI(Currency):

    PATH = "trades"

    def _get_unix_epoch(self, date: datetime) -> int:
        return int(date.timestamp())

    def _get_endpoint(
        self, /, date_from: datetime = None, date_to: datetime = None
    ) -> dict:

        url = f"{self.currency}/{self.PATH}/"

        if date_from:
            url += f"{self._get_unix_epoch(date_from)}/"

        elif date_to:
            assert date_from
            if date_from > date_to:
                raise RuntimeError("`date_from` should not be greater than `date_to`")
            url += f"{self._get_unix_epoch(date_to)}/"

        return url


if __name__ == "__main__":
    d = DaySummaryAPI("BTC")
    print(d.get_data(2019, 6, 26))

    t = TradeAPI("BTC")
    print(t.get_data())
    print(t.get_data(date_from=datetime(2021, 7, 4)))
    print(t.get_data(date_from=datetime(2021, 7, 4), date_to=datetime(2021, 7, 8)))
