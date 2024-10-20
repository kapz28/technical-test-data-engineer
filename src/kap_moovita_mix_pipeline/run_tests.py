# src/kap_moovita_mix_pipeline/run_tests.py

import pytest
import sys

def main():
    # Run pytest with any command line arguments passed to this script
    sys.exit(pytest.main(sys.argv[1:]))

if __name__ == "__main__":
    main()