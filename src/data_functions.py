"""Module for data functions."""

import pandas as pd


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


def build_budget(url_list):
    """
    Build a budget dataframe from a list of dataframes.
    """

    df_list = read_csvs(url_list)

    if not check_same_columns(df_list):
        raise ValueError("Dataframes do not have the same columns.")

    df_concat = concat_dataframes(df_list)

    return df_concat
