from datetime import datetime
from poo_module.src.ingestor.ingestor import DataIngestor
from poo_module.src.writer.writer import DataWriter

import pytest # type:ignore
from unittest.mock import mock_open, patch


@pytest.fixture
@patch("poo_module.src.ingestor.ingestor.DataIngestor.__abstractmethods__", set())
def data_ingestor_fixture():
    return DataIngestor(
        writer=DataWriter,
        currencies=["BTC", "ETH"],
        default_start_date=datetime(2021, 6, 21),
    )


@patch("poo_module.src.ingestor.ingestor.DataIngestor.__abstractmethods__", set())
class TestIngestors:
    def test_checkpoint_filename(self, data_ingestor_fixture):
        actual = data_ingestor_fixture._checkpoint_filename
        expected = "DataIngestor.checkpoint"
        assert actual == expected

    def test_load_checkpoint_no_checkpoint(self, data_ingestor_fixture):
        actual = data_ingestor_fixture._load_checkpoint()
        expected = None
        assert actual == expected

    @patch("builtins.open", new_callable=mock_open, read_data="2021-6-25")
    def test_load_checkpoint_existing_checkpoint(self, mock, data_ingestor_fixture):
        actual = data_ingestor_fixture._load_checkpoint()
        expected = datetime(2021, 6, 25)
        assert actual == expected

    @patch(
        "poo_module.src.ingestor.ingestor.DataIngestor._write_checkpoint",
        return_value=None,
    )
    def test_update_checkpoint_checkpoint_updated(self, mock, data_ingestor_fixture):
        expected = datetime(2019, 1, 1)
        di = data_ingestor_fixture
        di.checkpoint = expected
        assert di.checkpoint == expected
        mock.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data="2021-6-25")
    @patch(
        "poo_module.src.ingestor.ingestor.DataIngestor._checkpoint_filename",
        return_value="foobar.checkpoint",
    )
    def test_write_checkpoint(
        self, mock_checkpoint_file_name, mock_open, data_ingestor_fixture
    ):
        data_ingestor_fixture._write_checkpoint()
        mock_open.assert_called_with(mock_checkpoint_file_name, "w")
