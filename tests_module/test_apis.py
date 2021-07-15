from datetime import datetime, timedelta

import pytest
from random import sample, random, choice

from poo_module.src.api.currency_api import Currency, DaySummaryAPI, TradeAPI

def gen_dates():
    start_date = datetime(2016, 1, 1)
    end_date = datetime.today() - timedelta(days = 1)
    while True:
        yield start_date + random() * (end_date - start_date)

class TestDaySummaryAPI:

    @pytest.mark.parametrize(
        "currency, date, expected",
        [
            [currency, date, f"{currency}/day-summary/{date.year}/{date.month}/{date.day}/"]
            for currency, date in zip(
                sample(Currency.CURRENCIES, 5), 
                gen_dates()
            )
        ]
    )
    def test_get_endpoint(self, currency, date, expected):
        api = DaySummaryAPI(currency)
        actual = api._get_endpoint(date = date)
        assert actual == expected

class TestTradeAPI:

    @pytest.mark.parametrize(
        "currency, date_from, date_to, expected",
        [
        ]
    )
    def test_get_endpoint(self, currency, date_from, date_to, expected):
        api = TradeAPI(currency)
        actual = api._get_endpoint(date_from, date_to)
        assert actual == expected

    @pytest.mark.parametrize(
        'date, expected',
        [
        ]
    )
    def test_get_unix_epoch(self, date, expected):
        api = TradeAPI(choice(TradeAPI.CURRENCIES))
        assert api._get_unix_epoch(date) == expected

    @pytest.mark.parametrize(
        '',
        [
        ]
    )
    def test_get_endpoint_date_from_greater_than_date_to(self):
        with pytest.raises(RuntimeError):
            TradeAPI(currency = 'BTC')._get_endpoint(
                date_from = datetime(2021, 6, 15),
                date_to = datetime(2021, 6, 14),
            )