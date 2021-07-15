from datetime import datetime
from poo_module.src.ingestor.ingestor import DataIngestor
from poo_module.src.writer.writer import DataWriter

from unittest.mock import mock_open, patch


@patch("poo_module.src.ingestor.ingestor.DataIngestor.__abstractmethods__", set())
class TestIngestors:
    def test_checkpoint_filename(self):
        actual = DataIngestor(
            writer=DataWriter,
            currencies=["BTC", "ETH"],
            default_start_date=datetime(2021, 6, 21),
        )._checkpoint_filename
        expected = "DataIngestor.checkpoint"
        assert actual == expected

    def test_load_checkpoint_no_checkpoint(self):
        actual = DataIngestor(
            writer=DataWriter,
            currencies=["BTC", "ETH"],
            default_start_date=datetime(2021, 6, 21),
        )._load_checkpoint()
        expected = None
        assert actual == expected

    @patch("builtins.open", new_callable=mock_open, read_data="2021-6-25")
    def test_load_checkpoint_existing_checkpoint(self, mock):
        actual = DataIngestor(
            writer=DataWriter,
            currencies=["BTC", "ETH"],
            default_start_date=datetime(2021, 6, 21),
        )._load_checkpoint()
        expected = datetime(2021, 6, 25)
        assert actual == expected

    @patch(
        "poo_module.src.ingestor.ingestor.DataIngestor._write_checkpoint",
        return_value=None,
    )
    def test_update_checkpoint_checkpoint_updated(self, mock):
        di = DataIngestor(
            writer=DataWriter,
            currencies=["BTC", "ETH"],
            default_start_date=datetime(2021, 6, 21),
        )
        expected = datetime(2019, 1, 1)
        di.checkpoint = expected
        assert di.checkpoint == expected
