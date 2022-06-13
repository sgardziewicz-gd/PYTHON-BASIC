from statistics import mean
from lxml import etree


def check_result(xml_path: str):
    """Function to check weather XML file for Spain for 2021-09-25"""

    tree = etree.parse(xml_path)
    root = tree.getroot()

    assert root.tag == 'weather'
    assert not set(root.attrib.keys()).difference({'country', 'date'}), \
        "No 'country' or 'date' attrib in 'weather' root"

    children = root.getchildren()

    assert set([child.tag for child in children]) == {'summary', 'cities'}, \
        f'Invalid elements in "weather" root'

    for child in children:
        if child.tag == 'summary':
            summary_attribs = {'mean_temp', 'mean_wind_speed', 'coldest_place', 'warmest_place', 'windiest_place'}
            assert set(child.attrib.keys()) == summary_attribs, \
                f'Invalid attributes list in "summary" element: {set(child.attrib.keys()).difference(summary_attribs)}'
            summary = child.attrib

        if child.tag == 'cities':
            assert len([c for c in child]) == 17, f"Invalid number of cities in XML: {len([c for c in child])}"
            cities_summary = {}
            for city in child:
                city_attribs = {'mean_temp', 'mean_wind_speed',
                                'min_temp', 'min_wind_speed',
                                'max_temp', 'max_wind_speed'}
                assert set(city.attrib.keys()) == city_attribs, \
                    f"Invalid attributes in element {city.tag}: {set(city.attrib.keys()).difference(city_attribs)}"
                cities_summary[city.tag] = city.attrib

                if city.tag == 'Seville':
                    try:
                        assert float(city.attrib.get('mean_temp')) == 21.6
                        assert float(city.attrib.get('mean_wind_speed')) == 1.04
                        assert float(city.attrib.get('min_temp')) == 17.24
                        assert float(city.attrib.get('min_wind_speed')) == 0.45
                        assert float(city.attrib.get('max_temp')) == 27.13
                        assert float(city.attrib.get('max_wind_speed')) == 2.24
                    except AssertionError:
                        raise AssertionError("Incorrect values for random city.")

    # check results in summary
    mean_temp = round(mean([float(values['mean_temp']) for city, values in cities_summary.items()]), 2)
    assert float(summary['mean_temp']) == mean_temp, "Incorrect mean temperature in summary."

    assert summary.get('warmest_place') == 'Palma', \
        "The warmest place is incorrect"
    assert max(cities_summary.items(), key=lambda item: float(item[1].get('mean_temp')))[0] == summary.get('warmest_place'), \
        "The warmest place is incorrect. You need to find city with maximum mean temperature"

    assert summary.get('coldest_place') == 'Valladolid', \
        "The coldest place is incorrect"
    assert min(cities_summary.items(), key=lambda item: float(item[1].get('mean_temp')))[0] == summary.get('coldest_place'), \
        "The coldest place is incorrect. You need to find city with minimum mean temperature"

    assert summary.get('windiest_place') == 'Pamplona', \
        "The windiest place is incorrect"
    assert max(cities_summary.items(), key=lambda item: float(item[1].get('mean_wind_speed')))[0] == summary.get('windiest_place'), \
        "The coldest place is incorrect. You need to find city with maximum wind speed"

    print("Success!")


if __name__ == '__main__':
    check_result(xml_path='./Spain_weather.xml')
