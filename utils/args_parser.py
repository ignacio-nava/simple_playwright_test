import argparse

SEMAPHORE = 4
LAST_PAGINATION = 4
OUTPUT_FILE_NAME = 'products'
    
def parse():
    parser = argparse.ArgumentParser(description='Scrap Amazon with Playwright')
    parser.add_argument(
        '--semaphore', default=SEMAPHORE, type=int, help='an integer for the semaphore')
    parser.add_argument(
        '--last-pagination', default=LAST_PAGINATION, type=int, help='last page to search for')
    parser.add_argument(
        '--output-file-name', default=OUTPUT_FILE_NAME, help='output file name (extension not necessary)')

    args = parser.parse_args()
    return args.__dict__