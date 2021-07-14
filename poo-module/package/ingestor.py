from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from writer import DataWriter

from currency_api import DaySummaryAPI, TradeAPI

class DataIngestor(ABC):

    def __init__(self, writer: DataWriter, currencies: List[str], default_start_date: datetime):
        self._writer = writer
        self.currencies = currencies
        self.default_start_date = default_start_date

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
    def ingest(self, data) -> None:
        pass

class DaySummaryIngestor(DataIngestor):

    def __init__(self, writer: DataWriter, currencies: List[str], default_start_date: datetime):
        super().__init__(writer, currencies, default_start_date)

    def get_writer(self, api, currency, date):
        return self.writer(f'/{api.__class__.__name__}/{currency}/{date}.json')

    def ingest(self) -> None:

        date = self.default_start_date
        if date < datetime.today():
            for currency in self.currencies:
                api = DaySummaryAPI(currency = currency)
                writer = self.get_writer(api, currency, self._get_unix_epoch(date))
                data = api.get_data(date)
                writer.write(data)
                # TODO: update date

if __name__ == '__main__':
    dsi = DaySummaryIngestor(writer = DataWriter, currencies = ['BTC', 'ETH'], default_start_date = datetime(2021, 7, 13))
    dsi.ingest()