"""Module for main entry point for the application."""
import plotly.express as px
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

    cs = getattr(px.colors.sequential, col_scale='Reds_r')
    plot_treemap(bud23_exp, path=['Pääluokan nimi', 'Menoluvun nimi', 'Menomomentin nimi'],
                 col_scale=cs, drill_down_level=3)

    cs = getattr(px.colors.sequential, col_scale='Greens_r')
    plot_treemap(bud23_inc, path=['Osaston nimi', 'Tuloluvun nimi', 'Tulomomentin nimi'],
                 col_scale=cs, drill_down_level=3)


if __name__ == "__main__":
    main()
