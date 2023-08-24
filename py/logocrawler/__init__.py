from base_crawler import *
from csv_parser import *

path_to_urls_csv = "../../websites.csv"
output_path = "../data/output.csv"

if __name__ == '__main__':
    urls = read_from_csv(path_to_urls_csv)
    for url in urls:
        get_contents_from_url(url)

    a = logo_urls
    # print(logo_urls)
    # print((extract_logo_url_path_from_html('http://google.com', 'https://ly.lygo.net/ly/tpSite/images/tripodLogo.png')))
    # print(read_from_csv(path_to_urls_csv))
    write_to_csv(output_path, a)
