# test_scheduler.py

import pytest
import threading
import time
import ctypes
from kap_moovita_mix_pipeline.scheduler import start_scheduler
from kap_moovita_mix_pipeline import config

def terminate_thread(thread):
    """Terminates a python thread from another thread."""
    if not thread.is_alive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("Invalid thread ID")
    elif res != 1:
        # If it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def test_start_scheduler(capsys):
    # Arrange
    original_scheduled_time = config.SCHEDULED_TIME
    current_time = time.localtime(time.time() + 2)
    config.SCHEDULED_TIME = f"{current_time.tm_hour:02d}:{current_time.tm_min:02d}"

    # Act
    def run_scheduler():
        try:
            start_scheduler()
        except Exception as e:
            print(f"Scheduler stopped with error: {e}")
        except SystemExit:
            print("Scheduler terminated")

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # Wait for a short time to allow the scheduler to start
    time.sleep(3)

    # Assert
    captured = capsys.readouterr()

    # Check console output
    assert "Starting data flow in production mode." in captured.out
    assert f"Scheduled to run daily at {config.SCHEDULED_TIME}." in captured.out
    assert "Press Ctrl+C to exit." in captured.out

    # Clean up
    config.SCHEDULED_TIME = original_scheduled_time

    # Terminate the scheduler thread
    terminate_thread(scheduler_thread)
    
    # Wait for the thread to terminate
    scheduler_thread.join(timeout=2)
    
    if scheduler_thread.is_alive():
        pytest.fail("Failed to terminate the scheduler thread")
    
    final_capture = capsys.readouterr()
    assert "Scheduler terminated" in final_capture.out, "Scheduler did not terminate gracefully"

if __name__ == '__main__':
    pytest.main()