from lxml import html
import requests
from pymongo import MongoClient


URL = "https://lenta.ru"

headers = {
    "User-Agent": "curl/7.64.1",
    "Accept": "*/*"
}

client = MongoClient('localhost', 27017)
db = client['LentaDB']
news_collection = db['news']


def mongo_update_without_duplicate(collection, filter_, data):
    collection.update_one(filter_, data, upsert=True)


if __name__ == "__main__":
    response = requests.get(URL)
    print(f"Status code get request to {URL}: {response.status_code}")
    if 200 <= response.status_code <= 299:
        dom = html.fromstring(response.text)
        items = dom.xpath("//div[@class='span8 js-main__content']/section//div[@class='item'] "
                          "| //div[@class='span8 js-main__content']/section//div[@class='first-item']")
        news_data = []
        for item in items:
            src = URL + item.xpath(".//a/@href")[0]
            title = item.xpath(".//a/text()")[0]
            publication_date = item.xpath(".//time/@datetime")[0]
            news_data.append({
                "title": title,
                "src": src,
                "publication_date": publication_date
            })
            mongo_update_without_duplicate(news_collection, {"title": title, "src": src},
                                           {'$set': news_data[-1]})

    for news in news_data:
        print(news)


