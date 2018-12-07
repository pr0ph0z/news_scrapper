'''
Merdeka news scrapper
Search method is not supported here because they're using Google CSE (huh)
'''

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
        title = getContent(soup.find("meta", {"property": "og:title"}))
        url = getContent(soup.find("meta", {"property": "og:url"}))
        image = getContent(soup.find("meta", {"property": "og:image"}))
        author = getContent(soup.find("meta", {"name": "author"}))

        result = {
            "title": title,
            "url": url,
            "image": image,
            "author": author,
            "news": []
        }

        for i in filtered:
            search = re.compile('(?<=href=").*?(?=")')
            data = requests.get(search.search(i).group(0))
            data = data.content
            soup = BeautifulSoup(data, "html.parser")
            news = parseNews(soup.find("div", {"class": "mdk-body-paragpraph"}), "paging")

            result["news"].append(news)

        print(result)

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
        w = []
        subtitle = html.find("h6").get_text()
        subtitle = re.sub("\d\. ", "", subtitle)
        content = html.find("h6", {"class":"title-dt-paging"}).extract()
        subnews = html.get_text()
        subnews = re.sub("(^\\n\\n)|((Baca juga.*))", "", subnews)
        subnews = re.sub("(\\n)", " ", subnews)
        
        s.update({
            "subtitle": subtitle,
            "subnews": subnews
        })

        return s

def getContent(html):
    return html['content']

if __name__ == "__main__":
    # search("https://www.merdeka.com/cari/?q=prabowo")
    getNews("https://www.merdeka.com/politik/prediksi-prediksi-prabowo-subianto-yang-mengejutkan.html")