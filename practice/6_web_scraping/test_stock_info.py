import pytest
from stock_info import get_symbols, get_holders_data


def test_get_symbols_returns_correct_amount_of_symbols():
    symbols = get_symbols()
    assert len(symbols) == 25


def test_get_holders_data_returns_correct_amount_of_holders():
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36'
    headers = {'User-Agent': user_agent}
    cookies = {"cookie":"t=1655116572&j=1&u=1---&v=39"}
    holders = get_holders_data(headers, cookies)
    assert len(holders) == 10
