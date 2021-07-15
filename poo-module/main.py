
from schedule import repeat, every, run_pending
from datetime import datetime
from ingestor import DaySummaryIngestor, TradeIngestor
from writer import DataWriter


if __name__ == '__main__':
    currencies = ['BTC', 'ETH']
    default_start_date = datetime(2021, 7, 5)
    daysummary_ingestor = DaySummaryIngestor(writer = DataWriter, currencies = currencies, default_start_date = default_start_date)
    trade_ingestor = TradeIngestor(writer = DataWriter, currencies = currencies, default_start_date = default_start_date)

    @repeat(every(1).second)
    def job():
        daysummary_ingestor.ingest()
        trade_ingestor.ingest()
    
    while True:
        run_pending()