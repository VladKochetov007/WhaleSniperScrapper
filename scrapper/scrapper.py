import requests
from bs4 import BeautifulSoup

URL = "https://twitter.com/Whale_Sniper/status/1299074857271992320"
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
           'accept': '*/*'}
import time

def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def parse():
    html = get_html(URL)
    get_content(html.content)


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.text)

if __name__ == "__main__":
    parse()
