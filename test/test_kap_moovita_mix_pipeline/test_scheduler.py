# tests/test_kap_moovita_mix_pipeline/test_scheduler.py

import pytest
from unittest.mock import patch, MagicMock
from kap_moovita_mix_pipeline.scheduler import start_scheduler
from kap_moovita_mix_pipeline import config

# Fixture to mock the schedule module
@pytest.fixture
def mock_schedule():
    with patch('kap_moovita_mix_pipeline.scheduler.schedule') as mock:
        yield mock

# Fixture to mock the time module
@pytest.fixture
def mock_time():
    with patch('kap_moovita_mix_pipeline.scheduler.time') as mock:
        yield mock

# Fixture to mock the daily_data_retrieval function
@pytest.fixture
def mock_daily_data_retrieval():
    with patch('kap_moovita_mix_pipeline.scheduler.daily_data_retrieval') as mock:
        yield mock

def test_start_scheduler(mock_schedule, mock_time, mock_daily_data_retrieval, capsys):
    """
    Test the main functionality of the start_scheduler function.
    
    This test checks if:
    1. The scheduler is set up correctly
    2. The main loop runs and handles KeyboardInterrupt
    3. The correct messages are printed to the console
    """
    # Arrange: Set up the mock time.sleep to raise KeyboardInterrupt on second call
    mock_time.sleep.side_effect = [None, KeyboardInterrupt]  # Simulate Ctrl+C on second iteration
    
    # Act: Call the function under test
    start_scheduler()
    
    # Assert: Check the results
    captured = capsys.readouterr()  # Capture console output
    
    # Check if the scheduler is set up correctly
    mock_schedule.every().day.at.assert_called_once_with(config.SCHEDULED_TIME)
    mock_schedule.every().day.at().do.assert_called_once_with(mock_daily_data_retrieval)
    
    # Check if the main loop runs and handles KeyboardInterrupt
    mock_schedule.run_pending.assert_called_once()
    mock_time.sleep.assert_called_once_with(1)
    
    # Check console output
    assert f"Scheduled to run daily at {config.SCHEDULED_TIME}." in captured.out
    assert "Press Ctrl+C to exit." in captured.out
    assert "Script terminated by user." in captured.out
    assert "Shutting down scheduler..." in captured.out

@pytest.mark.parametrize("exception", [Exception("Test error"), KeyboardInterrupt()])
def test_start_scheduler_exception_handling(mock_schedule, mock_time, exception, capsys):
    """
    Test the exception handling in start_scheduler function.
    
    This test checks if:
    1. The function handles both KeyboardInterrupt and other exceptions
    2. The correct shutdown messages are printed for each case
    """
    # Arrange: Set up the mock time.sleep to raise the specified exception
    mock_time.sleep.side_effect = exception
    
    # Act: Call the function under test
    start_scheduler()
    
    # Assert: Check the results
    captured = capsys.readouterr()  # Capture console output
    
    # Check for appropriate message based on the type of exception
    if isinstance(exception, KeyboardInterrupt):
        assert "Script terminated by user." in captured.out
    else:
        assert "An error occurred:" in captured.out
    
    # Check if shutdown message is printed in all cases
    assert "Shutting down scheduler..." in captured.out
