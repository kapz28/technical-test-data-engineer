# tests/test_kap_moovita_mix_pipeline/test_data_processing.py

import pytest
from unittest.mock import Mock, patch
import json
from datetime import datetime
from kap_moovita_mix_pipeline.data_processing import (
    process_songs, process_users, process_listening_history, 
    update_metadata, process_data
)

@pytest.fixture
def mock_cursor():
    return Mock()

@pytest.fixture
def sample_songs_data():
    return {
        'items': [{'id': 1, 'name': 'Song 1'}, {'id': 2, 'name': 'Song 2'}],
        'total': 2,
        'pages': 1
    }

@pytest.fixture
def sample_users_data():
    return {
        'items': [{'id': 1, 'name': 'User 1'}, {'id': 2, 'name': 'User 2'}],
        'total': 2,
        'pages': 1
    }

@pytest.fixture
def sample_listening_history_data():
    return {
        'items': [
            {'user_id': 1, 'items': [{'song_id': 1}], 'created_at': '2023-01-01', 'updated_at': '2023-01-01'},
            {'user_id': 2, 'items': [{'song_id': 2}], 'created_at': '2023-01-02', 'updated_at': '2023-01-02'}
        ],
        'total': 2,
        'pages': 1
    }

def test_process_songs(mock_cursor, sample_songs_data):
    process_songs(mock_cursor, sample_songs_data)
    mock_cursor.executemany.assert_called_once()
    mock_cursor.execute.assert_called_once()
    assert mock_cursor.executemany.call_args[0][1] == sample_songs_data['items']

def test_process_users(mock_cursor, sample_users_data):
    process_users(mock_cursor, sample_users_data)
    mock_cursor.executemany.assert_called_once()
    mock_cursor.execute.assert_called_once()
    assert mock_cursor.executemany.call_args[0][1] == sample_users_data['items']

def test_process_listening_history(mock_cursor, sample_listening_history_data):
    process_listening_history(mock_cursor, sample_listening_history_data)
    mock_cursor.executemany.assert_called_once()
    mock_cursor.execute.assert_called_once()
    processed_items = mock_cursor.executemany.call_args[0][1]
    assert len(processed_items) == 2
    assert all('items' in item and isinstance(item['items'], str) for item in processed_items)

def test_update_metadata(mock_cursor):
    data_type = 'songs'
    total_items = 100
    total_pages = 10
    with patch('kap_moovita_mix_pipeline.data_processing.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 1, 1)
        update_metadata(mock_cursor, data_type, total_items, total_pages)
    mock_cursor.execute.assert_called_once()
    assert mock_cursor.execute.call_args[0][1] == (data_type, total_items, total_pages, '2023-01-01T00:00:00')

@pytest.mark.parametrize("data_type, expected_processor", [
    ('songs', process_songs),
    ('users', process_users),
    ('listening_history', process_listening_history),
    ('invalid_type', None)
])
def test_process_data(mock_cursor, data_type, expected_processor):
    sample_data = {'items': [], 'total': 0, 'pages': 0}
    with patch('kap_moovita_mix_pipeline.data_processing.PROCESSORS', {
        'songs': process_songs,
        'users': process_users,
        'listening_history': process_listening_history
    }):
        process_data(mock_cursor, data_type, sample_data)
    
    if expected_processor:
        mock_cursor.executemany.assert_called_once()
        mock_cursor.execute.assert_called_once()
    else:
        mock_cursor.executemany.assert_not_called()
        mock_cursor.execute.assert_not_called()

if __name__ == '__main__':
    pytest.main()