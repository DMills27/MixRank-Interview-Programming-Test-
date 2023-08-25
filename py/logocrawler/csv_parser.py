import csv
from functools import reduce
from typing import List, Tuple

def flatten_list(list_of_lists: List[List[str]]) -> List[str]:
    return reduce(lambda acc, sublist: acc + sublist, list_of_lists, [])

def line_formatter(line: str) -> str:
    return line if line.startswith("http") else "http://www." + line

def read_from_csv(file_path: str) -> List[str]:
    data_list = []
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data_list.append(list(map(line_formatter, row)))
    return flatten_list(data_list)

def write_to_csv(file_path: str, data_list: List[Tuple[str, str]]) -> None:
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for row in data_list:
            csv_writer.writerow(row)
