from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from pprint import pprint
import requests
import re

def search(url):
    data = requests.get(url)
    data = data.content
    soup = BeautifulSoup(data, "html.parser")
    results = soup.findAll("article")
    for result in results:
        getNews(result.a['href'])

def getNews(url):
    data = requests.get(url)
    data = data.content
    soup = BeautifulSoup(data, "html.parser")
    title = getContent(soup.find("meta", {"property": "og:title"}))
    url = getContent(soup.find("meta", {"property": "og:url"}))
    image = getContent(soup.find("meta", {"property": "og:image"}))
    author = getContent(soup.find("meta", {"name": "author"}))
    news = parseNews(soup.find("div", {"id": "detikdetailtext"}))

    result = {
        "title": title,
        "url": url,
        "image": image,
        "author": author,
        "news": news
    }

    print(news)

def parseNews(html):
    invalid_tags = ['p', 'a', 'br']
    p = html.find_all("p")
    if len(p) > 0:
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
    else:
        s = []
        for i in html:
            if type(i) is Tag or type(i) is Comment:
                i.extract()
        for i2 in html:
            if i2 is not '\n':
                print(i2)
                s.append(i2)
    return s

def getContent(html):
    return html['content']

if __name__ == "__main__":
    # search("https://www.detik.com/search/searchall?query=prabowo")
    getNews("https://news.detik.com/berita-jawa-tengah/d-4313269/cerita-prabowo-pernah-ditugasi-kejar-amien-rais-saat-orde-baru?_ga=2.249759430.1941936459.1542813273-658614994.1535639714")