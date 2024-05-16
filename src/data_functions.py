"""Module for data functions."""


import pandas as pd
import requests

from constants import BIG_MAC, TOTAL_CAPITA, \
    TOTAL_WORKING_AGE_CAPITA, GDP, MEDIAN_MONTHLY_SALARY, budget_units


from io import StringIO


def read_csvs(url_list):
    """
    Read a list of csv files and return a list of dataframes.
    """
    dataframes = []
    for url in url_list:
        print(f'reading {url}')
        df = pd.read_csv(url, encoding='ISO-8859-1', sep=';', decimal=',')
        df = df.apply(lambda x: x.str.replace(',', '')
                      if x.dtype == "object" else x)
        for col in df.columns:
            df[col] = df[col].map(lambda x: x.replace(
                '\xa0', ' ').strip() if isinstance(x, str) else x)

        dataframes.append(df)
    return dataframes


def check_same_columns(df_list):
    """
    Check if all dataframes in the list have the same columns.
    """

    first_df_columns = df_list[0].columns

    for df in df_list[1:]:
        if not df.columns.equals(first_df_columns):
            return False

    return True


def process_dataframe(df_list):
    """
    Process a DataFrame to keep only certain columns and rename one of them.
    """
    df_concat = pd.concat(df_list, ignore_index=True)

    df_concat = df_concat.filter(regex='nimi$|Määräraha')

    df_concat = df_concat.rename(columns={"Määräraha": "total"})

    return df_concat


def build_budget(url_list):
    """
    Build a budget dataframe from a list of dataframes.
    """

    df_list = read_csvs(url_list)

    if not check_same_columns(df_list):
        raise ValueError("Dataframes do not have the same columns.")

    df_concat = process_dataframe(df_list)

    return df_concat


def normalize_budget(df, method=None):
    """
    Normalize the budget dataframe.
    """
    df = df.copy()

    print(f'normalizing budget with method {method}')

    if method == 'beuros':
        df['total'] = (df['total'] / 10**9).round(1)
    elif method == 'percentage':
        df['total'] = df['total'] / df['total'].sum() * 100
    elif method == 'per_capita':
        df['total'] = df['total'] / TOTAL_CAPITA
    elif method == 'per_working_age_capita':
        df['total'] = df['total'] / TOTAL_WORKING_AGE_CAPITA
    elif method == 'big_mac':
        df['total'] = df['total'] / (BIG_MAC * TOTAL_CAPITA)
    elif method == 'gdp':
        df['total'] = df['total'] / GDP * 100
    elif method == 'median_monthly_salary':
        df['total'] = df['total'] / \
            (MEDIAN_MONTHLY_SALARY * TOTAL_WORKING_AGE_CAPITA)
    else:
        raise ValueError("Invalid normalization method.")

    return df


def budget_total_and_balance(df_inc, df_exp):
    """
    Calculate the total income and expenses and the balance.
    """

    df_inc = df_inc.copy()
    df_exp = df_exp.copy()

    total_income = df_inc['total'].sum()
    total_expenses = df_exp['total'].sum()

    net_loans = df_inc.loc[df_inc['Tulomomentin nimi'].str.strip(
    ).str.startswith('Net borrowing'), 'total'].values[0]

    net_income = total_income - net_loans
    balance = net_income - total_expenses

    return total_income, net_income, total_expenses, balance


def normalize_budget_data(budget_exp, budget_inc):
    """Normalize budget data using various methods."""
    methods = budget_units.keys()

    normalized_budgets = {}
    for method in methods:
        normalized_budgets[f'exp_{method}'] = normalize_budget(
            budget_exp, method=method)
        normalized_budgets[f'inc_{method}'] = normalize_budget(
            budget_inc, method=method)
    return normalized_budgets
