from datetime import datetime, timedelta
from os import stat

import requests

import pytest # type:ignore
from unittest.mock import patch
from random import sample, random, choice

from poo_module.src.api.currency_api import Currency, DaySummaryAPI, TradeAPI


def gen_dates():
    start_date = datetime(2016, 1, 1)
    end_date = datetime.today() - timedelta(days=1)
    while True:
        yield start_date + random() * (end_date - start_date)


def mock_requests_get(*args, **kwargs):
    class MockResponse(requests.Response):
        def __init__(self, json_data, status_code):
            super().__init__()
            self.status_code = status_code
            self.json_data = json_data

        def json(self):
            return self.json_data

        def raise_for_status(self) -> None:
            if self.status_code == 200:
                return None
            raise requests.RequestException

    if not args[0].endswith("invalid_endpoint"):
        return MockResponse(json_data={"foo": "bar"}, status_code=200)
    else:
        return MockResponse(json_data=None, status_code=500)


@pytest.fixture
@patch("poo_module.src.api.currency_api.Currency.__abstractmethods__", set())
def fixture_currency():
    return Currency(currency="BTC")


# @patch('poo_module.src.api.currency_api.Currency.__abstractmethods__', set())
class TestCurrency:
    @patch("requests.get", side_effect=mock_requests_get)
    @patch(
        "poo_module.src.api.currency_api.Currency._get_endpoint",
        return_value="valid_endpoint",
    )
    def test_get_data_requests_is_called(
        self, mock_get_endpoint, mock_requests, fixture_currency
    ):
        actual = fixture_currency.get_data()
        mock_requests.assert_called_once_with(Currency.BASE_URL + "valid_endpoint")

    @patch("requests.get", side_effect=mock_requests_get)
    @patch(
        "poo_module.src.api.currency_api.Currency._get_endpoint",
        return_value="valid_endpoint",
    )
    def test_get_data_with_valid_endpoint(
        self, mock_get_endpoint, mock_requests, fixture_currency
    ):
        actual = fixture_currency.get_data()
        expected = {"foo": "bar"}
        print("Actual: ", actual)
        assert actual == expected

    @patch("requests.get", side_effect=mock_requests_get)
    @patch(
        "poo_module.src.api.currency_api.Currency._get_endpoint",
        return_value="invalid_endpoint",
    )
    def test_get_data_with_invalid_endpoint(
        self, mock_get_endpoint, mock_requests, fixture_currency
    ):
        with pytest.raises(requests.RequestException):
            actual = fixture_currency.get_data()
            print("invalid: ", actual)


class TestDaySummaryAPI:
    @pytest.mark.parametrize(
        "currency, date, expected",
        [
            [
                currency,
                date,
                f"{currency}/day-summary/{date.year}/{date.month}/{date.day}/",
            ]
            for currency, date in zip(["BTC"], gen_dates())
            # for currency, date in zip(sample(DaySummaryAPI.CURRENCIES, 5), gen_dates())
            # TODO fix 5 currencies instead of using sample as its O(n)
        ],
    )
    def test_get_endpoint(self, currency, date, expected):
        api = DaySummaryAPI(currency)
        actual = api._get_endpoint(date=date)
        assert actual == expected


class TestTradeAPI:
    @pytest.mark.parametrize("currency, date_from, date_to, expected", [])
    def test_get_endpoint(self, currency, date_from, date_to, expected):
        api = TradeAPI(currency)
        actual = api._get_endpoint(date_from, date_to)
        assert actual == expected

    @pytest.mark.parametrize("date, expected", [])
    def test_get_unix_epoch(self, date, expected):
        api = TradeAPI(currency="BTC")
        assert api._get_unix_epoch(date) == expected

    @pytest.mark.parametrize("", [])
    def test_get_endpoint_date_from_greater_than_date_to(self):
        with pytest.raises(RuntimeError):
            TradeAPI(currency="BTC")._get_endpoint(
                date_from=datetime(2021, 6, 15),
                date_to=datetime(2021, 6, 14),
            )
