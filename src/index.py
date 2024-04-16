"""Module for main entry point for the application."""
from data_functions import build_budget
from config import BU23_EXP_URLS, BU23_INC_URLS


def main():
    """Main entry point for the application."""
    print("Hello, world!")

    # inc_list = read_csvs(BU23_INC_URLS)
    # exp_list = read_csvs(BU23_EXP_URLS)

    bud23_exp = build_budget(BU23_EXP_URLS)
    bud23_inc = build_budget(BU23_INC_URLS)

    print(bud23_exp)
    print(bud23_inc)
    print(bud23_exp.columns)
    print(bud23_inc.columns)


if __name__ == "__main__":
    main()
