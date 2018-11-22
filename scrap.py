from bs4 import BeautifulSoup
from pprint import pprint
import requests
import re

def search(url):
    data = requests.get(url)
    data = data.content
    soup = BeautifulSoup(data, "html.parser")
    results = soup.findAll("article")
    for result in results:
        pprint(result.a['href'])

def getNews(url):
    data = requests.get(url)
    data = data.content
    soup = BeautifulSoup(data, "html.parser")
    title = getContent(soup.find("meta", {"property": "og:title"}))
    image = getContent(soup.find("meta", {"property": "og:image"}))
    author = getContent(soup.find("meta", {"name": "author"}))
    news = parseNews(soup.find("div", {"id": "detikdetailtext"}))

    result = {
        "title": title,
        "image": image,
        "author": author,
        "news": news
    }

    print(result)

def parseNews(html):
    invalid_tags = ['p', 'a', 'br']
    p = html.find_all("p")
    s = []
    a = None
    for i in p:
        if(i.a):
            i.a.unwrap()
        if(i.br):
            i.br.extract()
        i.extract()
        content = str(i.contents)
        content = re.sub("^(\[')|(\[])|(\[\")|(\"])|\[<br\s*/?>\]", "", content)
        content = re.sub("(\'])$", " ", content)
        content = content.replace("', '", "")
        if content.strip():
            s.append(content+"\n")
    w = ''.join(map(str, s))
    return s

def getContent(html):
    return html['content']

if __name__ == "__main__":
    getNews("https://news.detik.com/berita/d-4311525/prabowo-sebut-air-laut-akan-sampai-hi-ini-solusi-anies")