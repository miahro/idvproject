"""Module for main entry point for the application."""
from data_functions import build_budget
from config import BU23_EXP_URLS, BU23_INC_URLS
from plot import plot_treemap


def main():
    """Main entry point for the application."""
    print("Hello, world!")

    # inc_list = read_csvs(BU23_INC_URLS)
    # exp_list = read_csvs(BU23_EXP_URLS)

    bud23_exp = build_budget(BU23_EXP_URLS)
    bud23_inc = build_budget(BU23_INC_URLS)

    # print(bud23_exp)
    # print(bud23_inc)
    # print(bud23_exp.columns)
    # print(bud23_inc.columns)

    plot_treemap(bud23_exp, path=[
                 'Pääluokan nimi', 'Menoluvun nimi', 'Menomomentin nimi'], drill_down_level=3)

    plot_treemap(bud23_inc, path=[
                 'Osaston nimi', 'Tuloluvun nimi', 'Tulomomentin nimi'], drill_down_level=3)


if __name__ == "__main__":
    main()
