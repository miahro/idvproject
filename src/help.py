"""Module for help content of the dashboard."""
import dash_html_components as html


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
            "Choose between viewing income or expenses with the radio buttons."),
        html.P(
            "Treemap graph shows hierachical data for the selected year and budget unit. "
            "Budget hierarchies are:"),
        html.Ul([
            html.Li("Class (Income type in income data, Ministry in expense data)"),
            html.Li("Category"),
            html.Li("Expense / income item (smallest details in the data)"),
            # Add more list items as needed
        ]),
        html.P(
            "The size of the rectangles represents the budget values. "
            "By placing mouse over the rectangles, "
            "you can see the details and values in hover window."),
        html.P(
            "You can drill down by clicking class, category or expense / income item "
            "rectangles to see more detailed data. To drill up from the detailed view, "
            "click category or class name (or grand total to return to main view)."),
    ])
