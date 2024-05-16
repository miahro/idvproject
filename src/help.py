"""Module for help content of the dashboard."""
from dash import html


def get_modal_content():
    """Return the content for the help modal."""
    return html.Div([
        html.P(
            "This dashboard allows you to view and analyze the Finnish state budget data."),
        html.P(
            "Use Budget unit(normalization to select units for budget values."),
        html.P(
            "Choose budget year with slider to view data for a specific year."),
        html.P(
            "Choose between viewing income or expenses with the radio buttons."
            "Income and expenses are shown in selected budget unit."),
        html.Ul([
            html.Li("Income means total income."),
            html.Li("Net income is total income minus loans."),
            html.Li("Expenses is total expenses."),
            html.Li("Budget balance means net income minus expenses."),
        ]),
        html.P(
            "Treemap graph shows hierachical data for the selected year and budget unit. "
            "Budget hierarchies are:"),
        html.Ul([
            html.Li("Class (Income type in income data, Ministry in expense data)"),
            html.Li("Category"),
            html.Li("Expense / income item (smallest details in the data)"),
        ]),
        html.P(
            "The size of the rectangles represents the budget values. "
            "By placing mouse over the rectangles, "
            "you can see the details and values in hover window."),
        html.P(
            "You can drill down by clicking class, category or expense / income item "
            "rectangles to see more detailed data. To drill up from the detailed view, "
            "click category or class name (or grand total to return to main view)."),
        html.P(
            "Budget units / normalizations used: "),
        html.Ul([
            html.Li("Billions of euros"),
            html.Li(
                "Per cent from total budget. Per cent from total expences or income, respectively"),
            html.Li("Euros per capita. Population 5.556 million (2023)"),
            html.Li(
                "Euros per working age capita. Working age population 3.121 million (2023)"),
            html.Li("Per cent of GDP 277.6 billion euros (2023)"),
            html.Li(
                "Big Macs per capita (per year). Big Mac price 7.55 euros (2024)"),
            html.Li(
                "Median Monthly Salaries per working age capita. Median salary 3215 euros (2023)"),
        ]),
    ])
