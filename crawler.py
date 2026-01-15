"""
bs4_crawling_pipeline.py
Web crawling pipeline using BeautifulSoup4.
"""

import requests
from bs4 import BeautifulSoup

def crawl_titles(url):
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch page")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.select(".titleline > a")

    for title in titles[:5]:
        print(title.text)

if __name__ == "__main__":
    url = "https://news.ycombinator.com/"
    crawl_titles(url)