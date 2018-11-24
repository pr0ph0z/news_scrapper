from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from pprint import pprint
import requests
import re
import bs4

def search(url):
    data = requests.get(url)
    data = data.content
    soup = BeautifulSoup(data, "html.parser")
    print(soup)
    # results = soup.findAll("article")
    # for result in results:
    #     getNews(result.a['href'])

def getNews(url):
    data = requests.get(url)
    data = data.content
    soup = BeautifulSoup(data, "html.parser")
    title = getContent(soup.find("meta", {"property": "og:title"}))
    url = getContent(soup.find("meta", {"property": "og:url"}))
    image = getContent(soup.find("meta", {"property": "og:image"}))
    author = getContent(soup.find("meta", {"name": "author"}))
    news = parseNews(soup.find("div", {"class": "mdk-body-paragpraph"}))

    result = {
        "title": title,
        "url": url,
        "image": image,
        "author": author,
        "news": news
    }

    # print("LAH")

def parseNews(html):
    html.find("div", {"class": "title-section_terkait"}).decompose()
    html.find("ul", {"id": "list-section_terkait"}).decompose()
    html.find("div").unwrap()
    pprint(len(html.get_text()))
    # return html

def getContent(html):
    return html['content']

if __name__ == "__main__":
    # search("https://www.merdeka.com/cari/?q=prabowo")
    getNews("https://www.merdeka.com/politik/prabowo-kesulitan-dana-kampanye-minta-kredit-dari-bank-indonesia-enggak-dapat.html")