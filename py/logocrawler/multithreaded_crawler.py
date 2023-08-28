from base_crawler import *
import requests
from bs4 import BeautifulSoup
import threading
from queue import Queue

def worker(queue):
    while True:
        url = queue.get()
        if url is None:
            break
        try:
            logo_links = get_contents_from_url(url)
            
            # Extract links and add to queue
            for link in logo_links:
                if new_url:
                    queue.put(link)
        except requests.RequestException as e:
            print("Error:", e)