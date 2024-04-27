"""Module for source data management"""

import os
import pandas as pd
from data_functions import build_budget, normalize_budget_data
from config import budget_urls


def get_or_save_data(url_list, filename):
    """
    Get data from a local file or online source.

    If use_saved_data is True and a local file with the given filename exists,
    load the DataFrame from the file. Otherwise, get the data from the online
    source and save it to a local file.
    """

    use_saved_data = os.getenv('USE_SAVED_DATA', 'True') == 'True'

    if use_saved_data and os.path.exists(filename):
        print(f"Loading data from {filename}")
        df = pd.read_csv(filename)
    else:
        print("accessing on-line data")
        df = build_budget(url_list)
        df.to_csv(filename, index=False)

    return df


def normalized_budgets_dict():
    """
    Return a dictionary with normalized budgets for all years.
    """

    normalized_budgets = {}

    for year, urls in budget_urls.items():
        print(f'loading data for year {year}')
        exp_urls, inc_urls = urls
        exp_data = get_or_save_data(exp_urls, f'data/bu{year}_exp.csv')
        inc_data = get_or_save_data(inc_urls, f'data/bu{year}_inc.csv')
        normalized_budgets[year] = normalize_budget_data(exp_data, inc_data)

    return normalized_budgets
