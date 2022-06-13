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
    symbols = []
    for tr in soup.find_all('a', {'class': 'Fw(600) C($linkColor)'}):
        symbols.append(tr.text)
    return symbols


def findCountry(stringText):
    countries = sorted([country.name for country in pycountry.countries] , key=lambda x: -len(x))
    for country in countries:
        if country.lower() in stringText.lower():
            return country
    return None

def get_number_of_employees(symbol):
    url = "https://finance.yahoo.com/quote/{}/profile?p={}".format(symbol, symbol)
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    headers = {'User-Agent': user_agent}
    cookies = {"cookie":"t=1655116572&j=1&u=1---&v=39"}
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    employees = soup.find_all('span', {'class': 'Fw(600)'})[2].text
    ceo_year_born = soup.find_all('td', {'class': 'Ta(end)'})[2].text
    ceo_name = soup.find_all('td', {'class': 'Ta(start)'})[0].text
    country = findCountry(soup.find_all('p', {'class': 'D(ib)'})[0].text)

    return employees, ceo_year_born, ceo_name, country

print(get_number_of_employees('AMZN'))



