import asyncio
import json
import pathlib

from utils.output_manager import write_csv
from utils.output_printer import finish_scrap
from utils.args_parser import parse

from sync_scrap.sync_scrap import sync_scrap
from async_scrap.async_scrap import async_scrap


def run(url, **kwargs):
    
    urls = sync_scrap(url)                               # Scrap URL for each category (simplify)
    products = asyncio.run(async_scrap(urls,  **kwargs)) # Scrap PRODUCTS for each URL
    return products

if __name__ == '__main__':
    kwargs = parse()

    ROOT = pathlib.Path().resolve()
    OUTPUT_FILES_DIR = ROOT / 'files'
    CONFIG_FILE = ROOT / 'config.json'
    
    with open(CONFIG_FILE, 'r') as config_file:
        config = json.load(config_file)
        url = config['url']
    products = run(url, **kwargs)
    
    csv_file_path = OUTPUT_FILES_DIR / f'{kwargs["output_file_name"]}.csv'
    pathlib.Path(csv_file_path).parents[0].mkdir(parents=True, exist_ok=True)
    headers = ['Id', 'Category', 'Name', 'Image', 'Price']
    write_csv(csv_file_path, headers, products)
    finish_scrap(csv_file_path)

