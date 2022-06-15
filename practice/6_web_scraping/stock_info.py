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

    return symbols


def findCountry(stringText):
    countries = sorted([country.name for country in pycountry.countries] , key=lambda x: -len(x))
    for country in countries:
        if country.lower() in stringText.lower():
            return country
    return None

def get_info_from_profile(symbol, headers, cookies):
    url = "https://finance.yahoo.com/quote/{}/profile?p={}".format(symbol, symbol)
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    profile_data = {
        'company_name' : soup.find('h3', {'class': 'Fz(m)'}).text,
        'code' : symbol,
        'country' : findCountry(soup.find_all('p', {'class': 'D(ib)'})[0].text),
        'employees' : soup.find_all('span', {'class': 'Fw(600)'})[2].text,
        'ceo_name' : soup.find_all('td', {'class': 'Ta(start)'})[0].text,
        'ceo_year_born' : soup.find_all('td', {'class': 'Ta(end)'})[2].text 
    }
    try:
        profile_data['company_name'] = soup.find('h3', {'class': 'Fz(m)'}).text
    except AttributeError:
        profile_data['company_name'] = "N/A"

    return profile_data


def get_info_from_statistics(symbol, headers, cookies):
    url = "https://finance.yahoo.com/quote/{}/key-statistics?p={}".format(symbol, symbol)
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    statistics_data = {
        'code' : symbol,
        '52_week_change' : soup.find_all('td', {'class':'Fw(500)'})[10].text
    }
    try:
        statistics_data['company_name'] = soup.find('h1', {'class':'Fz(18px)'}).text.rsplit(' ', 1)[0]
    except AttributeError:
        statistics_data['company_name'] = 'N/A'

    try:
        statistics_data['total_cash'] = soup.find_all('td', {'class':'Ta(end)'})[52].text
    except IndexError:
        statistics_data['total_cash'] = 'N/A'

    return statistics_data

def fill_symbols_with_statistics_info(symbols, headers, cookies):
    for symbol in symbols:
        symbols[symbol] = get_info_from_statistics(symbol, headers, cookies)
    return symbols


def fill_symbols_with_profile_info(symbols, headers, cookies):
    for symbol in symbols:
        symbols[symbol] = get_info_from_profile(symbol, headers, cookies)
    return symbols


def get_n_best_52_week_change_companies(n, symbols):
    symbols_sorted = sorted(symbols.items(), key=lambda x: float(x[1]['52_week_change'][:-1]) if x[1]['52_week_change'] != 'N/A' \
                                                                                              else -100.00, reverse=True)
    return symbols_sorted[:n]

def get_n_youngest_companies(n, symbols):
    symbols_sorted = sorted(symbols.items(), key=lambda x: int(x[1]['ceo_year_born']) if x[1]['ceo_year_born'] != 'N/A' \
                                                                                      else 0, reverse=True)
    return symbols_sorted[:n]

def append_holders(data_to_print, holders):
    for holder in holders.items():
        data_to_print.append([holder[1]['company_name'], holder[1]['shares'], holder[1]['date_reported'], holder[1]['out'], holder[1]['value']])

def append_best_52_week_change_data(data_to_print, best_n):
    for company in best_n:
        data_to_print.append([company[1]['company_name'], company[1]['code'], company[1]['52_week_change'], company[1]['total_cash']])

def append_youngest_ceos_data(data_to_print, youngest_5):
    for company in youngest_5:
        data_to_print.append([company[1]['company_name'], company[1]['code'], company[1]['country'],\
                            company[1]['employees'], company[1]['ceo_name'], company[1]['ceo_year_born']])


def print_sheet(column_names, title, stock_info, append_function):
    padding_spaces = (len(column_names) * 3) + 1
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

    print()


def get_holders_data(headers, cookies):
    url = "https://finance.yahoo.com/quote/BLK/holders?p=BLK"
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    holders = {}

    for tr in soup.find_all('td', {'class': 'Ta(start)'})[4:14]:
        holders[tr.text] = None
    details = []
    for tr in soup.find_all('td', {'class': 'Ta(end)'})[0:40]:
        details.append(tr.text)

    shares = details[0::4]
    date_reported = details[1::4]
    out = details[2::4]
    value = details[3::4]

    for i, holder in enumerate(holders):
        holders[holder] = {'company_name':holder, 'shares':shares[i], 'date_reported':date_reported[i], 'out':out[i], 'value':value[i]}

    return holders


def main():
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36'
    headers = {'User-Agent': user_agent}
    cookies = {"cookie":"t=1655116572&j=1&u=1---&v=39"}

    symbols = get_symbols()

    symbols_with_profile_info = fill_symbols_with_profile_info(symbols, headers, cookies)
    youngest_5 = get_n_youngest_companies(5, symbols_with_profile_info)
    column_names_youngest = (['Name', 'Code', 'Country', 'Employees', 'CEO Name', 'CEO Year Born'])
    title_youngest = '5 stocks with most youngest CEOs'
    print_sheet(column_names_youngest, title_youngest, youngest_5, append_youngest_ceos_data)

    symbols_with_statistics = fill_symbols_with_statistics_info(symbols, headers, cookies)
    best_10 = get_n_best_52_week_change_companies(10, symbols_with_statistics)
    column_names_best_52_week = (['Name', 'Code', '52-Week Change', 'Total Cash'])
    title_best_52_week = '10 stocks with best 52-Week change'
    print_sheet(column_names_best_52_week, title_best_52_week, best_10, append_best_52_week_change_data)

    column_names_holders = (['Name', 'Shares', 'Date Reported', '% Out', 'Value'])
    title_holders = '10 largest holders of Blackrock Inc.'
    holders = get_holders_data(headers, cookies)
    print_sheet(column_names_holders, title_holders, holders, append_holders)


if __name__ == '__main__':
    main()