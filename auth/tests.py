"""
This python file is used to run all the tests in the tests directory.

To run the tests, run the following command:
- python3 tests.py
"""

import unittest


if __name__ == '__main__':
    """
    This block of code is used to run all the tests in the tests directory.
    """
    loader = unittest.TestLoader()
    suite = loader.discover('./tests')
    runner = unittest.TextTestRunner()
    runner.run(suite)
