import requests
import concurrent.futures

API_KEY = "C49zTdqOxrrebvZe9U7px4NTs9425cfoaNSHVr69"
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_IMAGES = './output'


def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:
    url = f'{APOD_ENDPOINT}?api_key={api_key}&start_date={start_date}&end_date={end_date}'
    response = requests.get(url).json()
    url_list = [image_info['url'] for image_info in response if image_info['media_type'] == 'image']
    return url_list


def download_apod_images(metadata: list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:
        {executor.submit(download_image, url) for url in metadata}


def download_image(url: str):
    file_name = url.rsplit('/', 1)[1]
    with open(f'{OUTPUT_IMAGES}/{file_name}', 'wb') as f:
        f.write(requests.get(url).content)


def main():
    metadata = get_apod_metadata(
        start_date='2021-08-01',
        end_date='2021-09-30',
        api_key=API_KEY,
    )
    download_apod_images(metadata=metadata)


if __name__ == '__main__':
    main()
