# tests/test_kap_moovita_mix_pipeline/test_data_retrieval.py

import pytest
from unittest.mock import patch, MagicMock
from kap_moovita_mix_pipeline.data_retrieval import daily_data_retrieval
from kap_moovita_mix_pipeline import config

@pytest.fixture
def mock_sqlite3():
    with patch('kap_moovita_mix_pipeline.data_retrieval.sqlite3') as mock:
        yield mock

@pytest.fixture
def mock_fetch_all_data_types():
    with patch('kap_moovita_mix_pipeline.data_retrieval.fetch_all_data_types') as mock:
        yield mock

@pytest.fixture
def mock_processors():
    with patch('kap_moovita_mix_pipeline.data_retrieval.process_songs') as mock_songs, \
         patch('kap_moovita_mix_pipeline.data_retrieval.process_users') as mock_users, \
         patch('kap_moovita_mix_pipeline.data_retrieval.process_listening_history') as mock_history:
        yield {
            'songs': mock_songs,
            'users': mock_users,
            'listening_history': mock_history
        }

def test_daily_data_retrieval(mock_sqlite3, mock_fetch_all_data_types, mock_processors, capsys):
    # Arrange
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_sqlite3.connect.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_fetch_all_data_types.return_value = {
        'songs': {'data': 'songs_data'},
        'users': {'data': 'users_data'},
        'listening_history': {'data': 'history_data'}
    }

    # Act
    daily_data_retrieval()

    # Assert
    captured = capsys.readouterr()

    # Check database connection
    mock_sqlite3.connect.assert_called_once_with(config.DATABASE_NAME)
    
    # Check data fetching
    mock_fetch_all_data_types.assert_called_once()

    # Check data processing
    mock_processors['songs'].assert_called_once_with(mock_cursor, {'data': 'songs_data'})
    mock_processors['users'].assert_called_once_with(mock_cursor, {'data': 'users_data'})
    mock_processors['listening_history'].assert_called_once_with(mock_cursor, {'data': 'history_data'})

    # Check database commit
    mock_conn.commit.assert_called_once()

    # Check console output
    assert "Running daily data retrieval at" in captured.out
    assert "Processing songs data..." in captured.out
    assert "Processing users data..." in captured.out
    assert "Processing listening_history data..." in captured.out
    assert "All data processed and saved to the database." in captured.out
    assert "Daily data retrieval completed." in captured.out

def test_daily_data_retrieval_no_data(mock_sqlite3, mock_fetch_all_data_types, mock_processors, capsys):
    # Arrange
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_sqlite3.connect.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_fetch_all_data_types.return_value = {
        'songs': None,
        'users': None,
        'listening_history': None
    }

    # Act
    daily_data_retrieval()

    # Assert
    captured = capsys.readouterr()

    # Check that no data processing occurred
    for processor in mock_processors.values():
        processor.assert_not_called()

    # Check console output
    assert "No data received for songs" in captured.out
    assert "No data received for users" in captured.out
    assert "No data received for listening_history" in captured.out

if __name__ == '__main__':
    pytest.main()