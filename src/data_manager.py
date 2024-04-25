"""Module for source data management"""

import os
import pandas as pd
from data_functions import build_budget


def get_or_save_data(url_list, filename, use_saved_data=True):
    """
    Get data from a local file or online source.

    If use_saved_data is True and a local file with the given filename exists,
    load the DataFrame from the file. Otherwise, get the data from the online
    source and save it to a local file.
    """

    if use_saved_data and os.path.exists(filename):
        print(f"Loading data from {filename}")
        df = pd.read_csv(filename)
    else:
        print("accessing on-line data")
        df = build_budget(url_list)
        df.to_csv(filename, index=False)

    return df
