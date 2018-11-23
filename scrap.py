from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from pprint import pprint
import requests
import re
import bs4

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
        for i3 in html.find_all('br'):
            i3.extract()
        for i3 in html.find_all('table'):
            i3.extract()
        for i3 in html.find_all('strong'):
            i3.extract()
        for i2 in html:
            if "\n" not in i2:
                if i2.strip():
                    s.append(i2)
        s = ''.join(map(str, s))
    return html

def getContent(html):
    return html['content']

if __name__ == "__main__":
    # search("https://www.detik.com/search/searchall?query=prabowo")
    getNews("https://news.detik.com/berita/4314642/sebut-gaji-tukang-ojek-besar-tim-jokowi-makanya-pak-prabowo-gaul")