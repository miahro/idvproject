"""Module for source data management"""

import os
import csv
import pandas as pd
from data_functions import build_budget, normalize_budget_data
from config import budget_urls
from translation_dict import translations


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
        df = pd.read_csv(filename, encoding='utf-8')
    else:
        print("accessing on-line data")
        df = build_budget(url_list)
        df.insert(0, "Total budget", "Koko budjetti")
        df.to_csv(filename, index=False)

    return df


def read_csv_to_dict(filename):
    """reads translation csv file and returns a dictionary with translations"""

    with open(filename, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        data_dict = {}
        for i, row in enumerate(reader, start=1):
            try:
                key = row[0].strip('"')
                value = row[1].strip('"')
                if key in data_dict:
                    print(f"Duplicate key on line {i}: {row}")
                data_dict[key] = value
            except IndexError:
                print(f"IndexError on line {i}: {row}")
    return data_dict


def translate_budget_items(df, column_numbers=[0, 1, 2, 3]):  # pylint: disable=dangerous-default-value
    """
    Translate the values in a column to English.
    """

    if not isinstance(df, pd.DataFrame):
        print(f"Expected a DataFrame, but got {type(df)}")
        return df

    for col_num in column_numbers:
        col_name = df.columns[col_num]
        missing_keys = set(df[col_name]) - set(translations.keys())
        if missing_keys:
            print(f"Missing translations for keys: {missing_keys}")

        df[col_name] = df[col_name].map(translations).fillna(df[col_name])

    return df


def normalized_budgets_dict(translate=True):
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

    if translate:
        for year, budget_dict in normalized_budgets.items():
            if not isinstance(budget_dict, dict):
                print(
                    f"For year {year}, expected a dict but got {type(budget_dict)}")
                continue
            for method, df in budget_dict.items():
                if not isinstance(df, pd.DataFrame):
                    print(
                        f"For year {year} and method {method}, expect DF but got {type(df)}")
                    continue
                budget_dict[method] = translate_budget_items(df)

    return normalized_budgets
