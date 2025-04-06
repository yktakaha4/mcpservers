from mcp.server.fastmcp import FastMCP
import pandas as pd
import os
import glob

mcp = FastMCP("pandas")


@mcp.tool()
def list_datasets() -> list[str]:
    """list all datasets"""
    # list all datasets in the datasets directory
    datasets_dir = os.path.join(os.path.dirname(__file__), "datasets")
    return glob.glob(os.path.join(datasets_dir, "*.*"))
