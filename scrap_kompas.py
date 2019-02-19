'''
Kompas news scrapper
'''

from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from pprint import pprint
import requests
import re
import bs4

def getNews(url):
    data = requests.get(url)
    data = data.content
    soup = BeautifulSoup(data, "html.parser")
    title = getContent(soup.find("meta", {"property": "og:title"}))
    url = getContent(soup.find("meta", {"property": "og:url"}))
    image = getContent(soup.find("meta", {"property": "og:image"}))
    author = getContent(soup.find("meta", {"name": "author"}))
    news = parseNews(soup.find("div", {"class": "read__content"}))

    result = {
        "title": title,
        "url": url,
        "image": image,
        "author": author
    }

    print(news)

def parseNews(html):
    content = html.contents
    regex = re.compile("\\n")
    for i in content:
        print(str(i))

def getContent(html):
    return html['content']

if __name__ == "__main__":
    getNews("https://nasional.kompas.com/read/2018/12/11/13471861/presiden-jokowi-banyak-yang-ketakutan-dengan-kebijakan-satu-peta");