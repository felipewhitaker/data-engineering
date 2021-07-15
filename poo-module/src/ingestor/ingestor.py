from abc import ABC, abstractmethod
from typing import List

from datetime import datetime, timedelta

from api.currency_api import DaySummaryAPI, TradeAPI
from writer.writer import DataWriter



class DataIngestor(ABC):

    DATE_FORMAT = "%Y-%m-%d"

    def __init__(
        self, writer: DataWriter, currencies: List[str], default_start_date: datetime
    ):
        self._writer = writer
        self.currencies = currencies
        self.default_start_date = default_start_date
        self._checkpoint = self._load_checkpoint()

    @property
    def checkpoint(self) -> datetime:
        if not self._checkpoint:
            return self.default_start_date
        return self._checkpoint

    @checkpoint.setter
    def checkpoint(self, value):
        self._checkpoint = value
        self._write_checkpoint()

    @property
    def _checkpoint_filename(self):
        return f"{self.__class__.__name__}.checkpoint"

    def _write_checkpoint(self):
        with open(self._checkpoint_filename, "w") as f:
            f.write(f"{self.checkpoint.strftime(self.DATE_FORMAT)}")

    def _load_checkpoint(self):
        try:
            with open(self._checkpoint_filename, "r") as f:
                return datetime.strptime(f.read().strip(), self.DATE_FORMAT)
        except FileNotFoundError:
            return None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return True

    @staticmethod
    def _get_unix_epoch(date: datetime) -> int:
        return int(date.timestamp())

    @property
    def writer(self):
        return self._writer

    @abstractmethod
    def get_writer(self, /, *args, **kwargs):
        pass

    @abstractmethod
    def ingest(self, *args) -> None:
        pass


class DaySummaryIngestor(DataIngestor):

    api = DaySummaryAPI

    def __init__(
        self, writer: DataWriter, currencies: List[str], default_start_date: datetime
    ):
        super().__init__(writer, currencies, default_start_date)

    def get_writer(self, api, currency, date):
        return self.writer(
            f"{api.__class__.__name__}/{currency}/{date.strftime(self.DATE_FORMAT)}.json"
        )

    def ingest(self) -> None:

        date = self.checkpoint
        if date < datetime.today():
            for currency in self.currencies:
                api = self.api(currency=currency)
                writer = self.get_writer(api, currency, date)
                data = api.get_data(date)
                writer.write(data)
            self.checkpoint += timedelta(days=1)


class TradeIngestor(DataIngestor):

    DATE_FORMAT = "%Y-%m-%d_%H-%M-%S"
    api = TradeAPI

    def __init__(
        self, writer: DataWriter, currencies: List[str], default_start_date: datetime
    ):
        super().__init__(writer, currencies, default_start_date)
        raise NotImplemented
        # TODO implement date_from, date_to variables for ingestion

    def get_writer(self, currency, date_from, date_to):
        return self.writer(
            f"{self.api.__class__.__name__}/{currency}/{date_from.strftime(self.DATE_FORMAT)}.json"
        )

    def ingest(self) -> None:

        date = self.checkpoint
        if date < datetime.today():
            for currency in self.currencies:
                api = self.api(currency=currency)
                writer = self.get_writer(api, currency, date)
                data = api.get_data(date)  # TODO date_from and date_to
                writer.write(data)
            self.checkpoint += timedelta(days=1)
