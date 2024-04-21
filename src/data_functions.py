"""Module for data functions."""

import pandas as pd
from norm_factors import BIG_MAC, MILK_CARTON, PIZZA, TOTAL_CAPITA, \
    TOTAL_WORKING_AGE_CAPITA, GDP, MEDIAN_MONTHLY_SALARY


def read_csvs(url_list):
    """
    Read a list of csv files and return a list of dataframes.
    """

    dataframes = []
    for url in url_list:
        dataframes.append(pd.read_csv(
            url, encoding='ISO-8859-1', sep=';', decimal=','))
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


def concat_dataframes(df_list):
    """
    Concatenate all dataframes in the list into a single dataframe.
    """

    df_concat = pd.concat(df_list, ignore_index=True)

    start_columns = list(filter(lambda x: x.startswith(
        'Määräraha') or x.startswith('Aiemmin budjetoitu'), df_concat.columns))

    df_concat['total'] = df_concat.loc[:,
                                       start_columns[0]:start_columns[-1]].sum(axis=1)
    drop_columns = list(filter(lambda x: x.endswith(
        'info-osa') or x.startswith('Toteutuma') or x.endswith('numero'), df_concat.columns))

    df_concat = df_concat.drop(columns=start_columns + drop_columns)

    return df_concat


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

    # df_concat = concat_dataframes(df_list)
    df_concat = process_dataframe(df_list)
    # print(df_concat.shape)

    print(df_concat.head())

    return df_concat


def normalize_budget(df, method=None):
    """
    Normalize the budget dataframe.
    """

    # df = build_budget(url_list)

    df = df.copy()

    if method == 'beuros':
        df['total'] = (df['total'] / 10**9).round(1)
    elif method == 'percentage':
        df['total'] = (df['total'] / df['total'].sum() * 100).round(1)
    elif method == 'per_capita':
        df['total'] = (df['total'] / TOTAL_CAPITA).round(1)
    elif method == 'per_working_age_capita':
        df['total'] = (df['total'] / TOTAL_WORKING_AGE_CAPITA).round(1)
    elif method == 'big_mac':
        df['total'] = (df['total'] / (BIG_MAC * TOTAL_CAPITA)).round(1)
    elif method == 'gdp':
        df['total'] = (df['total'] / GDP).round(1)
    elif method == 'milk_cartons':
        df['total'] = (df['total'] / (MILK_CARTON * TOTAL_CAPITA)).round(1)
    elif method == 'pizzas':
        df['total'] = (df['total'] / (PIZZA * TOTAL_CAPITA)).round(1)
    elif method == 'median_monthly_salary':
        df['total'] = (df['total'] /
                       (MEDIAN_MONTHLY_SALARY * TOTAL_WORKING_AGE_CAPITA)).round(1)
    else:
        raise ValueError("Invalid normalization method.")
    # print(f'normalized with {method} method')
    # print(df.describe())

    return df


def budget_total_and_balance(df_inc, df_exp):
    """
    Calculate the total income and expenses and the balance.
    """

    df_inc = df_inc.copy()
    df_exp = df_exp.copy()

    total_income = df_inc['total'].sum()
    total_expenses = df_exp['total'].sum()

    net_loans = df_inc.loc[df_inc['Tulomomentin nimi'].str.startswith(
        'Nettolainanotto'), 'total'].values[0]

    net_income = total_income - net_loans

    print(f"total: {net_loans}")
    balance = net_income - total_expenses

    print(
        f'total income: {total_income}, net income: {net_income} total expenses:'
        f'{total_expenses}, balance: {balance}'
    )

    return net_income, total_expenses, balance
