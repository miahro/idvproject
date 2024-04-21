"""Helper module to collect links from budjetti.vm.fi webpage."""

import requests
from bs4 import BeautifulSoup


def extract_links(url):
    """Extract all links from a webpage."""
    response = requests.get(url, timeout=5)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)
    base_url = 'https://budjetti.vm.fi'
    return [base_url + link['href'] for link in links]


def filter_csv_links(links):
    """Filter out links that end with '.csv'."""
    csv_lnks = []
    for lnk in links:
        if lnk.endswith('.csv'):
            csv_lnks.append(lnk)
    return csv_lnks


WEBPAGE_URL = ('https://budjetti.vm.fi/indox/opendata/2023/tae'
               '/eduskunnanKirjelma/2023-tae-eduskunnanKirjelma.html'
               )


all_links = extract_links(WEBPAGE_URL)


csv_links = filter_csv_links(all_links)

for link in csv_links:
    print(f"'{link}',")
