import os
import unittest
import unittest.mock

import pandas as pd

import src.main

TEST_DATASETS_BASE_DIR = os.path.join(os.path.dirname(__file__), "datasets")


@unittest.mock.patch(
    "src.main.get_datasets_base_dir", return_value=TEST_DATASETS_BASE_DIR
)
class TestMain(unittest.TestCase):
    def test_load_dataset(self, _):
        actual = src.main.load_dataset("titanic.tsv")
        self.assertIsInstance(actual, pd.DataFrame)

    def test_load_dataset_not_found(self, _):
        with self.assertRaises(FileNotFoundError):
            src.main.load_dataset("non_existent.tsv")

    def test_load_dataset_unsupported_format(self, _):
        with self.assertRaises(ValueError):
            src.main.load_dataset("data.unsupported")

    def test_list_datasets(self, _):
        actual = src.main.list_datasets()
        self.assertIn("titanic.tsv", actual)

    def test_describe_dataset_tsv(self, _):
        actual = src.main.describe_dataset("titanic.tsv")

        self.assertIsInstance(actual, dict)
        self.assertIn("PassengerId", actual["columns"])
        self.assertEqual(actual["describe"]["PassengerId"]["count"], 891.0)

    def test_query_dataset(self, _):
        actual = src.main.query_dataset("titanic.tsv", "PassengerId == 1")
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0]["PassengerId"], 1)

    def test_query_dataset_with_orderby(self, _):
        actual = src.main.query_dataset(
            "titanic.tsv", query="Age > '30'", orderby=["Age", "PassengerId"]
        )
        self.assertEqual(len(actual), 514)
        self.assertEqual(actual[0]["Age"], "30.5")
