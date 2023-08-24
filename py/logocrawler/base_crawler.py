import re
import requests
from requests.models import Response
from typing import List
from bs4 import BeautifulSoup

#Convert this to a frozenset to prevent any unexected modifications/mutations that may occur when scaling up.
#This can occur with multithreading/concurrency etc.
#It's genuinely better to always have an immutable data structure in situations like these.
logo_urls = []

def get_contents_from_url(_url: str)-> List[str]:
    try:
        #Attempts to get a response and times out if not received within 3 seconds
        response = requests.get(_url, timeout=3) 
        # Checks whether the page redirects to another url. 
        # If it does then get the redirected url is saved as the new url as adding it the original url may result in a 404.
        if response.status_code == 301:
            html_content = BeautifulSoup(response._content, "html.parser")
            #Gets information associated with the canonical url from the HTML body
            canonical = html_content.find('link', {'rel': 'canonical'})
            redirected_url = canonical['href']
            end = get_logo_path(redirected_url, response)
        elif response.status_code == requests.codes.ok:
            end = get_logo_path(_url, response)
            print(end)
        else:
            logo_urls.append((_url, "403: The requested resource is forbidden"))
    except requests.exceptions.Timeout:
        logo_urls.append((_url,"Timeout"))
    except requests.exceptions.ConnectionError:
        logo_urls.append((_url,"Connection Error"))

def extract_logo_url_path_from_html(_url: str, path: str) -> str:
    #Checks whether the path is a URL or relative path to it. Also, cleans the url and path.
    return list(map(lambda part: url.rstrip('/') + '/' + part.lstrip('/') if not part.startswith('http') else part, [path]))[0]

def get_logo_path(_url, _response: Response) -> str:
        temporary_list_for_logos = []
        parsed_response = _response.text
        html_dom = BeautifulSoup(parsed_response, "html.parser")
        #Uses the metadata in the class and alt attributes to determine if logos are present and scrapable 
        logos_within_class_attr, logos_within_alt_attr  = html_dom.find_all(['a','img', 'div'],  {'class': re.compile("(?i)logo")}), html_dom.find_all(['a','img', 'div'],  {'alt': re.compile("(?i)logo")})
        elements = logos_within_class_attr + logos_within_alt_attr
        #Checks if a source tag is present then captures the link present if it is add it to the list.
        for html_element in elements:
            if html_element.get('src'):
                temporary_list_for_logos.append(html_element.get('src'))
            else:
                temporary_list_for_logos.append(None)
        # 
        if all(element is None for element in temporary_list_for_logos):
            logo_urls.append((_url, "No logos to scrape"))
        else:
            first_logo_path = next(item for item in temporary_list_for_logos if item is not None)
            logo_urls.append((_url, first_logo_path))
        return logo_urls