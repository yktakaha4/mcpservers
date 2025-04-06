import glob
import json
import os

import pandas as pd
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pandas")
cached_datasets = {}


def get_datasets_base_dir() -> str:
    return os.path.join(os.path.dirname(__file__), "..", "datasets")


def load_dataset(dataset_name: str) -> pd.DataFrame:
    """load a dataset"""
    if dataset_name not in cached_datasets:
        dataset_file_path = os.path.join(get_datasets_base_dir(), dataset_name)
        if not os.path.exists(dataset_file_path):
            raise FileNotFoundError(f"Dataset {dataset_name} not found")

        dataframe = None
        if dataset_name.endswith(".tsv"):
            dataframe = pd.read_csv(dataset_file_path, sep="\t")

        if dataframe is not None:
            cached_datasets[dataset_name] = dataframe
        else:
            raise ValueError(f"Unsupported file format for dataset {dataset_name}")

    return cached_datasets[dataset_name]


@mcp.tool()
def list_datasets() -> list[str]:
    """list all dataset names"""
    return [
        os.path.basename(f)
        for f in glob.glob(os.path.join(get_datasets_base_dir(), "*.*"))
    ]


@mcp.tool()
def describe_dataset(dataset_name: str) -> dict:
    """describe a dataset"""
    dataset = load_dataset(dataset_name)
    return {
        "columns": dataset.columns.tolist(),
        "dtypes": dataset.dtypes.astype(str).to_dict(),
        "shape": dataset.shape,
        "describe": json.loads(dataset.describe(include="all").to_json()),
    }


@mcp.tool()
def query_dataset(
    dataset_name: str,
    query: str = None,
    orderby: list[str] = None,
) -> list[dict]:
    """query a dataset"""
    dataset = load_dataset(dataset_name)
    if query:
        dataset = dataset.query(query)
    if orderby:
        dataset = dataset.sort_values(orderby)

    return dataset.to_dict(orient="records")
