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


WEBPAGE_URL = ('https://budjetti.vm.fi/indox/opendata/2024/tae'
               '/eduskunnanKirjelma/2024-tae-eduskunnanKirjelma.html'
               )


# WEBPAGE_URL = ('https://budjetti.vm.fi/indox/opendata/2023/tae'
#                '/eduskunnanKirjelma/2023-tae-eduskunnanKirjelma.html'
#                )

# WEBPAGE_URL = ('https://budjetti.vm.fi/indox/opendata/2019/tae'
#                '/eduskunnanKirjelma/2019-tae-eduskunnanKirjelma.html'
#                )

# WEBPAGE_URL = ('https://budjetti.vm.fi/indox/opendata/2014/tae'
#                '/eduskunnanKirjelma/2014-tae-eduskunnanKirjelma.html'
#                )


# WEBPAGE_URL = ('https://budjetti.vm.fi/indox/opendata/2024/tae'
#                '/eduskunnanKirjelma/2024-tae-eduskunnanKirjelma.html'
#                )

# WEBPAGE_URL = ('https://budjetti.vm.fi/indox/opendata/2022/tae'
#                '/eduskunnanKirjelma/2022-tae-eduskunnanKirjelma.html'
#                )

# WEBPAGE_URL = ('https://budjetti.vm.fi/indox/opendata/2021/tae'
#                '/eduskunnanKirjelma/2021-tae-eduskunnanKirjelma.html'
#                )

# WEBPAGE_URL = ('https://budjetti.vm.fi/indox/opendata/2020/tae'
#                '/eduskunnanKirjelma/2020-tae-eduskunnanKirjelma.html'
#                )

# WEBPAGE_URL = ('https://budjetti.vm.fi/indox/opendata/2018/tae'
#                '/eduskunnanKirjelma/2018-tae-eduskunnanKirjelma.html'
#                )

# WEBPAGE_URL = ('https://budjetti.vm.fi/indox/opendata/2017/tae'
#                '/eduskunnanKirjelma/2017-tae-eduskunnanKirjelma.html'
#                )


# WEBPAGE_URL = ('https://budjetti.vm.fi/indox/opendata/2016/tae'
#                '/eduskunnanKirjelma/2016-tae-eduskunnanKirjelma.html'
#                )


# WEBPAGE_URL = ('https://budjetti.vm.fi/indox/opendata/2015/tae'
#                '/eduskunnanKirjelma/2015-tae-eduskunnanKirjelma.html'
#                )

all_links = extract_links(WEBPAGE_URL)


csv_links = filter_csv_links(all_links)

for link in csv_links:
    print(f"'{link}',")
