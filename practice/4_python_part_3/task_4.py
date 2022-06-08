"""
Create virtual environment and install Faker package only for this venv.
Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.
Exec format:
`$python task_4.py NUMBER --FIELD=PROVIDER [--FIELD=PROVIDER...]`
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider
Example:
`$python task_4.py 2 --fake-address=address --some_name=name`
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}
"""

import argparse
import sys
import faker




### Modified to run like: 'python task_4.py 2 --data fake-address=address fake-name=name'
def print_name_address(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("number")
    parser.add_argument("--data", nargs='+')
    args = parser.parse_args()
    number = int(args.number)
    d = {}
    for item in args.data:
        i = item.split('=')
        d[i[0]] = i[1]

    print_from_kwargs(number, d)
    

def print_from_kwargs(number: int, dict) -> None:
    fake=faker.Faker()

    for i in range(number):
        result = {}
        for key, value in dict.items():
            fake_function = getattr(fake, value)
            result[key] = fake_function()
        print(result)
    

#print_name_address(sys.argv[1:])



"""
Write test for print_name_address function
Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 123
    >>> m.method()
    123
"""
from unittest.mock import patch



@patch('faker.providers.person.Provider.name', side_effect=["Testowy Chlop"])
@patch('faker.providers.address.Provider.address', side_effect=["Testowy Adres"])
def test_print_from_kwargs(mock1, mock2, capfd):
    test_dict = {"fake_name":"name", "fake_adress":"address"}
    print_from_kwargs(1, test_dict)
    out, err = capfd.readouterr()
    assert out == "{'fake_name': 'Testowy Chlop', 'fake_adress': 'Testowy Adres'}\n"
