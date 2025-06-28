import unittest
import argparse
from unittest.mock import patch
from tabulate import tabulate
from main import main


class TestMain(unittest.TestCase):

    @patch('argparse.ArgumentParser.parse_args')
    def test_main_aggregate(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            file=None,
            where=None,
            aggregate="price=min"
        )
        self.assertEqual(main(), tabulate([{'column': 'price', 'min': 149}], headers='keys', tablefmt='outline'))

        mock_parse_args.return_value = argparse.Namespace(
            file="products.csv",
            where="price=1199",
            aggregate=None
        )
        self.assertEqual(main(), tabulate([{'name': 'galaxy s23 ultra', 'brand': 'samsung', 'price': 1199, 'rating': 4.8}],
                                          headers='keys', tablefmt='outline'))

    @patch('main.read_csv')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_without_params(self, mock_parse_args, mock_read_csv):
        data = [
            {'name': 'iphone 15 pro', 'brand': 'apple', 'price': '999', 'rating': '4.9'},
        ]
        mock_read_csv.return_value = data
        mock_parse_args.return_value = argparse.Namespace(
            file=None,
            where=None,
            aggregate=None
        )
        self.assertEqual(main(), tabulate(data, headers='keys', tablefmt='outline'))


if __name__ == "__main__":
    unittest.main()
