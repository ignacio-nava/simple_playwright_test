from .output_manager import get_len_file

def finish_scrap(file_path):
    print(' SCRAP FINISHED '.center(40, '·'))
    print(f'Total products scraped: {get_len_file(file_path)}')
    print(''.center(40, '·'))