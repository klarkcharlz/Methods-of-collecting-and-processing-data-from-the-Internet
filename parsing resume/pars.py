import requests
from bs4 import BeautifulSoup
from loguru import logger

import argparse


logger.add('log/log.log', format='{time} {level} {message}', level='DEBUG')

parser = argparse.ArgumentParser()
parser.add_argument(
    '--url',
    type=str,
    default=None,
    help='Link(url) to resume. Default = None.'
)
args = parser.parse_args()

if __name__ == "__main__":
    url = args.url
    logger.info(f"Принят URL: {url}\nДелаем запрос по заданному url...")
    headers = {
        "User-Agent": "curl/7.64.1",
        "Accept": "*/*"
    }
    response = requests.get(url, headers=headers)
    logger.info(f"Запрос выполнен, статус ответа: {response.status_code}!")
    soup = BeautifulSoup(response.text, 'html.parser')
    logger.info("Начинаем парсить...")

    position = soup.findAll("h1", {"data-qa": "vacancy-title"})[0].text
    logger.info(position)
