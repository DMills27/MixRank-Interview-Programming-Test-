from base_crawler import *
from csv_parser import *

path_to_urls_csv = "../../websites.csv"
output_path = "../data/output.csv"

if __name__ == '__main__':
    urls = read_from_csv(path_to_urls_csv)
    for url in urls:
        get_contents_from_url(url)

    cleansed_urls = cleanse_logo_urls(logo_urls)
    write_to_csv(output_path, cleansed_urls)