import re
import requests
from requests.models import Response
from typing import List, Tuple
from bs4 import BeautifulSoup

# Convert this to a frozenset to prevent any unexected modifications/mutations that may occur when scaling up.
# This can occur with multithreading/concurrency etc.
# It's genuinely better to always have an immutable data structure in situations like these.
logo_urls = []

def get_contents_from_url(_url: str)-> List[str]:
    try:
        # Attempts to get a response and times out if not received within 3 seconds
        response = requests.get(_url, timeout=3) 
        # Checks whether the page redirects to another url. 
        # If it does then get the redirected url is saved as the new url as adding it the original url may result in a 404.
        if response.status_code == 301:
            html_content = BeautifulSoup(response._content, "html.parser")
            # Gets information associated with the canonical url from the HTML body
            canonical_header_info = html_content.find('link', {'rel': 'canonical'})
            redirected_url = canonical_header_info['href']
            logo_paths = get_logo_path(redirected_url, response)
            return logo_paths
        elif response.status_code == requests.codes.ok:
            logo_paths = get_logo_path(_url, response)
            return logo_paths
        else:
            logo_urls.append((_url, "403: The requested resource is forbidden"))
    except requests.exceptions.Timeout:
        logo_urls.append((_url,"A timeout occurred when trying to reach this url"))
    except requests.exceptions.ConnectionError:
        logo_urls.append((_url,"A connection error occurred when trying to reach this url"))

def get_logo_path(_url: str, _response: Response) -> str:
    temporary_list_for_logos = []
    parsed_response = _response.text
    html_dom = BeautifulSoup(parsed_response, "html.parser")
    # Uses the metadata in the class and alt attributes to determine if logos are present and scrapable 
    logos_within_class_attr, logos_within_alt_attr  = html_dom.find_all(['a','img', 'div'],  {'class': re.compile("(?i)logo")}), html_dom.find_all(['a','img', 'div'],  {'alt': re.compile("(?i)logo")})
    elements = logos_within_class_attr + logos_within_alt_attr
    # Checks if a source tag is present then captures the link present if it is add it to the list.
    for html_element in elements:
        if html_element.get('src'):
            temporary_list_for_logos.append(html_element.get('src'))
        else:
            temporary_list_for_logos.append(None)
    # Checks if all the elements in the logo_urls list is populated with None i.e. if no logos were able to be scraped.
    if all(element is None for element in temporary_list_for_logos):
        logo_urls.append((_url, "No logos to scrape"))
    else:
        # Finds the first non-None element in the list and and selects that as the candidate for our logo url
        # Need a better heuristic for determining whether this is indeed a valid logo. 
        first_logo_path = next(item for item in temporary_list_for_logos if item is not None)
        logo_urls.append((_url, first_logo_path))
    return logo_urls

# Below is a function to clean and normalise the links for the logo urls that were extracted from get_logo_path function.
# Valid extracted logo data from scraping websites appear as either urls or uris. These need to be normalised as urls by
# concatenating the site urls with the links that appear as uris.
def refine_logo_urls(logo_tuple: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    first_element, second_element = logo_tuple
    # Check if the data from the logo src tag was already normalised
    if second_element.startswith("http"):
        return logo_tuple
    # Check if the source was a data URI scheme e.g. data:image/png; 
    elif second_element.startswith("data:"):
        new_second_element = f"No path to logo asset; just a data URI scheme"
        return (first_element, new_second_element)
    else:
        # Modify the logo path tuple element to normalise it
        new_second_element = f"{first_element}{second_element}"
        return (first_element, new_second_element)

# The function below separates the list of websites that have relevant extracted information about websites against those where no information about the logo could not be generated.
# It then normalises the logo url links (in the sense of generating complete urls that point to the logo assest) and then combines it with the list of sites of which no logo information was found.
def cleanse_logo_urls(_logo_urls):
    list_of_urls_with_no_logo_data = list(filter(lambda tup: not tup[1].startswith("http") and not tup[1].startswith("/") and not tup[1].startswith("data"), _logo_urls))
    list_of_urls_with_cleansed_logo_data = list(map(refine_logo_urls, filter(lambda tup: tup[1].startswith("http") or tup[1].startswith("/") or tup[1].startswith("data"), _logo_urls)))
    cleansed_logo_urls = list_of_urls_with_cleansed_logo_data + list_of_urls_with_no_logo_data
    return cleansed_logo_urls