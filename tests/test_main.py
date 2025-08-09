import datetime
import os
import sys
from unittest import mock

# Ensure local src package is importable
TEST_DIR = os.path.dirname(__file__)
SRC_ROOT = os.path.join(TEST_DIR, "..", "src")
sys.path.insert(0, SRC_ROOT)
sys.path.insert(0, os.path.join(SRC_ROOT, "demonlab_dashboard"))

from demonlab_dashboard.main import GridLayoutTest


def test_query_db_next_datapoint():
    app = GridLayoutTest()
    fake_cursor = mock.Mock()
    fake_cursor.fetchone.return_value = (
        "Next Datapoint",
        datetime.datetime(2025, 1, 1, 12, 0, 0),
    )
    fake_conn = mock.Mock()
    fake_conn.cursor.return_value = fake_cursor

    with mock.patch("psycopg2.connect", return_value=fake_conn):
        result = app.query_db_next_datapoint()

    assert result == "Next Datapoint: 2025-01-01 12:00:00"
    fake_cursor.execute.assert_called()
    fake_cursor.close.assert_called_once()
    fake_conn.close.assert_called_once()


def test_query_db_next_datapoint_no_data():
    app = GridLayoutTest()
    fake_cursor = mock.Mock()
    fake_cursor.fetchone.return_value = None
    fake_conn = mock.Mock()
    fake_conn.cursor.return_value = fake_cursor

    with mock.patch("psycopg2.connect", return_value=fake_conn):
        result = app.query_db_next_datapoint()

    assert result == "Next Datapoint: N/A"
    fake_cursor.close.assert_called_once()
    fake_conn.close.assert_called_once()
