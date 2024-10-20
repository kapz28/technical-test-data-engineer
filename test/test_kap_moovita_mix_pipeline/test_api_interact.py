# tests/test_kap_moovita_mix_pipeline/test_api_interact.py

import pytest
from unittest.mock import patch, Mock
from kap_moovita_mix_pipeline.api_interact.api_interaction import APIClient, get_all_data_for_type, fetch_all_data_types, ENDPOINTS
from kap_moovita_mix_pipeline import config
import requests

@pytest.fixture
def mock_requests():
    """Fixture to mock the requests library"""
    with patch('kap_moovita_mix_pipeline.api_interact.requests') as mock:
        yield mock

@pytest.fixture
def api_client():
    """Fixture to create an instance of APIClient"""
    return APIClient()

def test_api_client_initialization():
    """Test APIClient initialization"""
    client = APIClient()
    assert client.base_url == config.BASE_URL

    custom_url = "http://custom.api.com"
    client_custom = APIClient(custom_url)
    assert client_custom.base_url == custom_url

def test_fetch_data_success(api_client, mock_requests):
    """Test successful data fetching"""
    mock_response = Mock()
    mock_response.json.return_value = {"data": "test"}
    mock_requests.get.return_value = mock_response

    result = api_client.fetch_data("/test")
    assert result == {"data": "test"}
    mock_requests.get.assert_called_once_with(f"{config.BASE_URL}/test")

def test_fetch_data_failure(api_client, mock_requests):
    """Test data fetching failure"""
    mock_requests.get.side_effect = requests.RequestException("Test error")

    result = api_client.fetch_data("/test")
    assert result is None

def test_fetch_all_data(api_client, mock_requests):
    """Test fetching all paginated data"""
    mock_responses = [
        {"items": [1, 2], "total": 5, "pages": 3},
        {"items": [3, 4], "total": 5, "pages": 3},
        {"items": [5], "total": 5, "pages": 3},
    ]

    mock_requests.get.side_effect = [Mock(json=lambda: resp) for resp in mock_responses]

    result = api_client.fetch_all_data("/test")
    assert result == {"items": [1, 2, 3, 4, 5], "total": 5, "pages": 3}
    assert mock_requests.get.call_count == 3

def test_get_all_data_for_type(mock_requests):
    """Test getting all data for a specific type"""
    with patch('kap_moovita_mix_pipeline.api_interact.api_client.fetch_all_data') as mock_fetch:
        mock_fetch.return_value = {"items": [1, 2, 3]}
        
        result = get_all_data_for_type('songs')
        assert result == {"items": [1, 2, 3]}
        mock_fetch.assert_called_once_with(ENDPOINTS['songs'])

def test_get_all_data_for_invalid_type():
    """Test getting data for an invalid type"""
    result = get_all_data_for_type('invalid_type')
    assert result is None

def test_fetch_all_data_types(mock_requests):
    """Test fetching data for all types"""
    mock_data = {"items": [1, 2, 3]}
    
    with patch('kap_moovita_mix_pipeline.api_interact.get_all_data_for_type', return_value=mock_data) as mock_get:
        result = fetch_all_data_types()
        
        assert result == {data_type: mock_data for data_type in ENDPOINTS}
        assert mock_get.call_count == len(ENDPOINTS)

@pytest.mark.parametrize("endpoint", ENDPOINTS.values())
def test_endpoints(endpoint):
    """Test that all endpoints are valid"""
    assert endpoint.startswith('/')
