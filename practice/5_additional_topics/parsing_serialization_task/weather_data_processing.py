import json
import os
from termios import CINTR


def get_hourly_from_city(path):
    with open(path, 'r') as f:
        return json.load(f)['hourly']


def get_temp_and_wind_speed(data_hourly):
    temp = []
    wind_speed = []
    for entry in data_hourly:
        temp.append(entry['temp'])
        wind_speed.append(entry['wind_speed'])
    return temp, wind_speed


def calculate_statistics(temp, wind_speed):
    city_stats = {}
    city_stats['temp_min'] = round(min(temp), 2)
    city_stats['temp_max'] = round(max(temp), 2)
    city_stats['temp_mean'] = round((sum(temp) / len(temp)), 2)
    city_stats['wind_min'] = round(min(wind_speed), 2)
    city_stats['wind_max'] = round(max(wind_speed), 2)
    city_stats['wind_mean'] = round(sum(wind_speed) / len(wind_speed), 2)
    return city_stats


def get_stats_from_city(path_to_city):
    data_hourly = get_hourly_from_city(path_to_city)
    temp, wind_speed = get_temp_and_wind_speed(data_hourly)
    city_stats = {}
    city_stats = calculate_statistics(temp, wind_speed)
    return city_stats


def get_path_of_cities(source_data_path):
    file_paths = []
    for root, _, files in os.walk(source_data_path, topdown=False, onerror=None):
        for file in files:
            if file.endswith(".json"):
                file_paths.append(os.path.join(root, file))
    return file_paths


def get_stats_for_all_cities(list_of_paths):
    all_cities = {}
    for city_path in list_of_paths:
        path = os.path.dirname(city_path)
        city_name = os.path.basename(path)
        all_cities[city_name] = get_stats_from_city(city_path)
    return all_cities


def calculate_country_stats(all_cities):
    temp_sum = 0
    wind_sum = 0
    coldest_temp = 1000.0
    warmest_temp = -1000.0
    fastest_wind = 0.0

    for k, v in all_cities.items():
        #print(k, v['temp_mean'])
        temp_sum = temp_sum + v['temp_mean']
        wind_sum = wind_sum + v['wind_mean']
        if v['temp_mean'] < coldest_temp:
            coldest_temp = v['temp_mean']
            coldest_place = k
        if v['temp_mean'] > warmest_temp:
            warmest_temp = v['temp_mean']
            warmest_place = k
        if v['wind_mean'] > fastest_wind:
            fastest_wind = v['wind_mean']
            windiest_place = k

    country_temp_mean = round(temp_sum / len(all_cities.items()), 2)
    country_wind_mean = round(wind_sum / len(all_cities.items()), 2)
    return country_temp_mean, country_wind_mean, coldest_place, warmest_place, windiest_place


def get_date_from_path(list_of_paths):
    date =  os.path.basename(list_of_paths[0]).split('.')[0]
    return date.replace('_', '-')


def generate_xml(country_name, path):
    list_of_paths = get_path_of_cities(path)
    all_cities = get_stats_for_all_cities(list_of_paths)
    all_cities = dict(sorted(all_cities.items()))
    country_temp, country_wind, coldest_place, warmest_place, windiest_place = calculate_country_stats(all_cities)
    date = get_date_from_path(list_of_paths)

    xml = [f'<weather country="{country_name}" date="{date}">']
    xml.append(f'  <summary mean_temp="{country_temp}" mean_wind_speed="{country_wind}" coldest_place="{coldest_place}" warmest_place="{warmest_place}" windiest_place="{windiest_place}"/>')
    xml.append(f'  <cities>')
    for k, v in all_cities.items():
        xml.append(f'    <{k.replace(" ", "-")} mean_temp="{v["temp_mean"]}" mean_wind_speed="{v["wind_mean"]}" min_temp="{v["temp_min"]}" min_wind_speed="{v["wind_min"]}" max_temp="{v["temp_max"]}" max_wind_speed="{v["wind_max"]}" />')
    xml.append(f'  </cities>')
    xml.append(f'</weather>')
    with open(f'{country_name}_weather.xml', 'w') as f:
        f.write('\n'.join(xml))


#long_path = "/Users/sgardziewicz/Python Basics/PYTHON-BASIC/practice/5_additional_topics/parsing_serialization_task/source_data"
test_data_short_path = "./tests/example_data"
spain_data_path = "./source_data"

generate_xml('Spain', spain_data_path)

