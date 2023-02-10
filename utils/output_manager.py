import csv

def write_csv(file_path, headers, data):
    with open(file_path, 'w', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows([(i, *values) for i, values in enumerate(data)])
        file.close()

def get_len_file(file_path):
    count = -1
    with open(file_path, 'r', encoding='UTF8') as file:
        reader = csv.reader(file)
        for row in reader:
            count += 1
    return count