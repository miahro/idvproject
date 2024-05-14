"""Module for constants"""

budget_units = {
    'beuros': 'Billions of euros',
    'percentage': 'Per cent from total budget',
    'per_capita': 'Euros per capita',
    'per_working_age_capita': 'Euros per working age capita',
    'gdp': 'Per cent of GDP',
    'big_mac': 'Big Macs per capita (per year)',
    'milk_cartons': 'Milk Cartons per capita (per year)',
    'pizzas': 'Pizzas per capita (per year)',
    'median_monthly_salary': 'Median Monthly Salaries per working age capita'
}


BIG_MAC = 7.55
MILK_CARTON = 1.25
PIZZA = 10.00
TOTAL_CAPITA = 5.556*10**6
TOTAL_WORKING_AGE_CAPITA = 3.121*10**6
GDP = 277.6*10**9
MEDIAN_MONTHLY_SALARY = 3215

color_scales = {
    'reds_r': ['rgb(103, 0, 13)', 'rgb(138, 9, 18)', 'rgb(170, 16, 22)',
               'rgb(192, 21, 27)', 'rgb(213, 34, 33)', 'rgb(234, 54, 42)',
               'rgb(244, 79, 57)', 'rgb(251, 106, 74)', 'rgb(252, 129, 97)',
               'rgb(252, 152, 121)', 'rgb(252, 175, 148)', 'rgb(253, 198, 175)',
               'rgb(254, 219, 203)', 'rgb(254, 233, 223)', 'rgb(255, 245, 240)'],
    'greens_r': ['rgb(0,68,27)', 'rgb(0,109,44)', 'rgb(35,139,69)', 'rgb(65,171,93)',
                 'rgb(116,196,118)', 'rgb(161,217,155)', 'rgb(199,233,192)',
                 'rgb(229,245,224)', 'rgb(247,252,245)']
}
