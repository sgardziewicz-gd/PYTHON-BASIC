import json
import os


path_to_city_short = 'tests/example_data/Brest/2021_09_25.json'
path_to_city = '/Users/sgardziewicz/Python Basics/PYTHON-BASIC/practice/5_additional_topics/parsing_serialization_task/tests/example_data/Brest/2021_09_25.json'


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
    city_stats['temp_min'] = min(temp)
    city_stats['temp_max'] = max(temp)
    city_stats['temp_mean'] = sum(temp) / len(temp)
    city_stats['wind_min'] = min(wind_speed)
    city_stats['wind_max'] = max(wind_speed)
    city_stats['wind_mean'] = sum(wind_speed) / len(wind_speed)
    return city_stats


def get_stats_from_city(path_to_city):
    data_hourly = get_hourly_from_city(path_to_city)
    temp, wind_speed = get_temp_and_wind_speed(data_hourly)
    city_stats = {}
    city_stats['stats'] = calculate_statistics(temp, wind_speed)
    return city_stats


def get_path_of_cities(source_data_path):
    file_paths = []
    for root, _, files in os.walk(source_data_path, topdown=False, onerror=None):
        for file in files:
            if file.endswith(".json"):
                file_paths.append(os.path.join(root, file))
    return file_paths

long_path = "/Users/sgardziewicz/Python Basics/PYTHON-BASIC/practice/5_additional_topics/parsing_serialization_task/source_data"

test_data_short_path = "./tests/example_data"

list_of_paths = get_path_of_cities(test_data_short_path)
#list_of_paths = get_path_of_cities(long_path)
all_cities = {}
for city_path in list_of_paths:
    path = os.path.dirname(city_path)
    city_name = os.path.basename(path)
    all_cities[city_name] = get_stats_from_city(city_path)

# print(all_cities)
# print(3)

print(all_cities["Minsk"]["stats"])
print(type(all_cities))

def calculate_country_stats(all_cities_dict):
    temp_sum = 0
    wind_sum = 0
    coldest_temp = 1000.0
    warmest_temp = -1000.0
    fastest_wind = 0.0

    for k, v in all_cities.items():
        print(k, v['stats']['temp_mean'])
        temp_sum = temp_sum + v['stats']['temp_mean']
        wind_sum = wind_sum + v['stats']['wind_mean']
        if v['stats']['temp_mean'] < coldest_temp:
            coldest_temp = v['stats']['temp_mean']
            coldest_place = k
        if v['stats']['temp_mean'] > warmest_temp:
            warmest_temp = v['stats']['temp_mean']
            warmest_place = k
        if v['stats']['wind_mean'] > fastest_wind:
            fastest_wind = v['stats']['wind_mean']
            windiest_place = k

    country_temp_mean = temp_sum / len(all_cities.items())
    country_wind_mean = wind_sum / len(all_cities.items())

    return country_temp_mean, country_wind_mean, coldest_place, warmest_place, windiest_place


country_temp, country_wind, coldest_place, warmest_place, windiest_place = calculate_country_stats(all_cities)

print(f"temp mean{country_temp}, wind mean{country_wind}")
print(coldest_place)
print(warmest_place)
print(windiest_place)
