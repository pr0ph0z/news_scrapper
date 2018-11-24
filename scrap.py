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

    if soup.find("ul", {"class": "mdk-list-paging"}) is None:
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

        print(result)
    else:
        a = soup.select("ul[class=mdk-list-paging] li a")
        regex_arrow = re.compile('<a class="arrow.*"></a>')
        regex_intro = re.compile('<a href=".*">Intro</a>')
        filtered = [str(i) for i in a if not regex_arrow.search(str(i)) and not regex_intro.search(str(i))]

        for i in filtered:
            search = re.compile('(?<=href=").*?(?=")')
            data = requests.get(search.search(i).group(0))
            data = data.content
            soup = BeautifulSoup(data, "html.parser")
            title = getContent(soup.find("meta", {"property": "og:title"}))
            url = getContent(soup.find("meta", {"property": "og:url"}))
            image = getContent(soup.find("meta", {"property": "og:image"}))
            author = getContent(soup.find("meta", {"name": "author"}))
            news = parseNews(soup.find("div", {"class": "mdk-body-paragpraph"}), "paging")

            result = {
                "title": title,
                "url": url,
                "image": image,
                "author": author,
                "news": news
            }

            print(news)

def parseNews(html, article_type = "normal"):
    if article_type is "normal":
        s = []
        html.find("div", {"class": "title-section_terkait"}).decompose()
        html.find("ul", {"id": "list-section_terkait"}).decompose()
        html.find("div").unwrap()
        for i in html.get_text().split("\n"):
            if i.strip():
                i = re.sub(" \[(.*?)]", "", i)
                s.append(i)
        s = '\n'.join(map(str, s))
        text_file = open("output_test.txt", "w")
        text_file.write(s)
        text_file.close()
    else:
        s  = {}
        title = html.find("h6").get_text()
        title = re.sub("\d\. ", "", title)
        s.update({
            "title": title
        })

    return html

def getContent(html):
    return html['content']

if __name__ == "__main__":
    # search("https://www.merdeka.com/cari/?q=prabowo")
    getNews("https://www.merdeka.com/politik/prediksi-prediksi-prabowo-subianto-yang-mengejutkan.html")