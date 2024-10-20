# tests/test_kap_moovita_mix_pipeline/test_api_interact.py

import pytest
import requests
from unittest.mock import Mock, patch
from kap_moovita_mix_pipeline.api_interact.api_interaction import APIClient, get_all_data_for_type, fetch_all_data_types, ENDPOINTS
from kap_moovita_mix_pipeline import config

@pytest.fixture
def api_client():
    return APIClient()

def test_api_client_initialization():
    client = APIClient()
    assert client.base_url == config.BASE_URL

    custom_url = "http://custom.api.com"
    client_custom = APIClient(custom_url)
    assert client_custom.base_url == custom_url

@patch('kap_moovita_mix_pipeline.api_interact.api_interaction.requests.get')
def test_fetch_data_success(mock_get, api_client):
    mock_response = Mock()
    mock_response.json.return_value = {"data": "test"}
    mock_get.return_value = mock_response

    result = api_client.fetch_data("/test")
    assert result == {"data": "test"}
    mock_get.assert_called_once_with(f"{config.BASE_URL}/test")

@patch('kap_moovita_mix_pipeline.api_interact.api_interaction.requests.get')
def test_fetch_data_failure(mock_get, api_client):
    mock_get.side_effect = requests.RequestException("Test error")

    result = api_client.fetch_data("/test")
    assert result is None
    mock_get.assert_called_once_with(f"{config.BASE_URL}/test")

@patch('kap_moovita_mix_pipeline.api_interact.api_interaction.requests.get')
def test_fetch_all_data(mock_get, api_client):
    mock_responses = [
        Mock(json=lambda: {"items": [1, 2], "total": 3, "pages": 2}),
        Mock(json=lambda: {"items": [3], "total": 3, "pages": 2}),
    ]
    mock_get.side_effect = mock_responses

    result = api_client.fetch_all_data("/test")
    assert result == {"items": [1, 2, 3], "total": 3, "pages": 2}
    assert mock_get.call_count == 2

@patch('kap_moovita_mix_pipeline.api_interact.api_interaction.APIClient.fetch_all_data')
def test_get_all_data_for_type(mock_fetch):
    mock_fetch.return_value = {"items": [1, 2, 3]}
    
    result = get_all_data_for_type('songs')
    assert result == {"items": [1, 2, 3]}
    mock_fetch.assert_called_once_with(ENDPOINTS['songs'])

def test_get_all_data_for_invalid_type():
    result = get_all_data_for_type('invalid_type')
    assert result is None

@patch('kap_moovita_mix_pipeline.api_interact.api_interaction.get_all_data_for_type')
def test_fetch_all_data_types(mock_get_all_data):
    mock_data = {"items": [1, 2, 3]}
    mock_get_all_data.return_value = mock_data
    
    result = fetch_all_data_types()
    
    assert result == {data_type: mock_data for data_type in ENDPOINTS}
    assert mock_get_all_data.call_count == len(ENDPOINTS)

@pytest.mark.parametrize("endpoint", ENDPOINTS.values())
def test_endpoints(endpoint):
    assert endpoint.startswith('/')