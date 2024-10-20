# tests/test_kap_moovita_mix_pipeline/test_cli.py

import pytest
from unittest.mock import patch
import io
import sys
from kap_moovita_mix_pipeline.cli import setup_cli, display_config_help, display_current_config
from kap_moovita_mix_pipeline import config

def test_setup_cli():
    """
    Test the setup_cli function to ensure it correctly parses command-line arguments.
    """
    # Test with no arguments
    with patch('sys.argv', ['script_name']):
        args = setup_cli()
        assert not args.test
        assert not args.info
        assert not args.help_config

    # Test with --test argument
    with patch('sys.argv', ['script_name', '--test']):
        args = setup_cli()
        assert args.test
        assert not args.info
        assert not args.help_config

    # Test with --info argument
    with patch('sys.argv', ['script_name', '--info']):
        args = setup_cli()
        assert not args.test
        assert args.info
        assert not args.help_config

    # Test with --help-config argument
    with patch('sys.argv', ['script_name', '--help-config']):
        args = setup_cli()
        assert not args.test
        assert not args.info
        assert args.help_config

def test_display_config_help(capsys):
    """
    Test the display_config_help function to ensure it prints the correct help information.
    """
    display_config_help()
    captured = capsys.readouterr()
    
    # Check if the output contains expected information
    assert "Configuration Help:" in captured.out
    assert "BASE_URL:" in captured.out
    assert "SCHEDULED_TIME:" in captured.out
    assert "Example .env file content:" in captured.out

def test_display_current_config(capsys):
    """
    Test the display_current_config function to ensure it prints the current configuration correctly.
    """
    display_current_config()
    captured = capsys.readouterr()
    
    # Check if the output contains the current configuration
    assert "Current Configuration:" in captured.out
    assert f"API Base URL: {config.BASE_URL}" in captured.out
    assert f"Scheduled Run Time: {config.SCHEDULED_TIME}" in captured.out