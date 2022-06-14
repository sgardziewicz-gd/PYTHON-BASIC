"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet

Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""

import requests
import pycountry
from bs4 import BeautifulSoup


def get_symbols():
    url = "https://finance.yahoo.com/most-active"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    symbols = {}
    i = 0
    for tr in soup.find_all('a', {'class': 'Fw(600) C($linkColor)'}):
        symbols[tr.text] = None
        # i += 1
        # if i > 5:
        #     break
    return symbols


def findCountry(stringText):
    countries = sorted([country.name for country in pycountry.countries] , key=lambda x: -len(x))
    for country in countries:
        if country.lower() in stringText.lower():
            return country
    return None

def get_info_from_profile(symbol):
    url = "https://finance.yahoo.com/quote/{}/profile?p={}".format(symbol, symbol)
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36'
    headers = {'User-Agent': user_agent}
    cookies = {"cookie":"t=1655116572&j=1&u=1---&v=39"}
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    profile_data = {
        'company_name' : soup.find('h3', {'class': 'Fz(m)'}).text,
        'code' : symbol,
        'country' : findCountry(soup.find_all('p', {'class': 'D(ib)'})[0].text),
        'employees' : soup.find_all('span', {'class': 'Fw(600)'})[2].text,
        'ceo_name' : soup.find_all('td', {'class': 'Ta(start)'})[0].text,
        'ceo_year_born' : '1900' if soup.find_all('td', {'class': 'Ta(end)'})[2].text == 'N/A'\
                                 else soup.find_all('td', {'class': 'Ta(end)'})[2].text
    }
    return profile_data


def fill_symbols_with_info(symbols):
    for symbol in symbols:
        symbols[symbol] = get_info_from_profile(symbol)
    return symbols


def get_n_youngest_companies(n, symbols):
    symbols_sorted = sorted(symbols.items(), key=lambda x: x[1]['ceo_year_born'], reverse=True)
    return symbols_sorted[:n]


def append_youngest_ceos_data(data_to_print, youngest_5):
    for company in youngest_5:
        data_to_print.append([company[1]['company_name'], company[1]['code'], company[1]['country'],\
                            company[1]['employees'], company[1]['ceo_name'], company[1]['ceo_year_born']])


def print_sheet(column_names, title, padding_spaces, stock_info, append_function):
    data_to_print = []
    data_to_print.append(column_names)
    append_function(data_to_print, stock_info)
    widths = [max(map(len, col)) for col in zip(*data_to_print)]
    longest_row_character_length = sum(widths)
    centered_title = title.center(longest_row_character_length+padding_spaces, '=')
    separator = ''.center(longest_row_character_length+padding_spaces, '-')
    print(centered_title)
    del data_to_print[0]
    print ("| " + " | ".join((val.ljust(width) for val, width in zip(column_names, widths))) + " |")
    print(separator)
    for row in data_to_print:
        print ("| " + " | ".join((val.ljust(width) for val, width in zip(row, widths))) + " |")
    print('\n')


def main():
    symbols = get_symbols()
    symbols = fill_symbols_with_info(symbols)
    youngest_5 = get_n_youngest_companies(5, symbols)

    column_names = (['Name', 'Code', 'Country', 'Employees', 'CEO Name', 'CEO Year Born'])
    title = '5 stocks with most youngest CEOs'
    padding_spaces = 19

    print_sheet(column_names, title, padding_spaces, youngest_5, append_youngest_ceos_data)


if __name__ == '__main__':
    main()