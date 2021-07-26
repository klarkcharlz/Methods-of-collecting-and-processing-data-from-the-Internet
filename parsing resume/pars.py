"""
Необходимо собрать информацию о вакансиях на вводимую должность
(используем input или через аргументы) с сайтов Superjob и HH.
Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (отдельно минимальную и максимальную).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas.
Можно выполнить по желанию один любой вариант или оба при желании и возможности.
"""

import requests
from bs4 import BeautifulSoup
from loguru import logger
from pandas import DataFrame
from tabulate import tabulate

import argparse
from urllib.parse import urlparse
from collections import defaultdict


logger.add('log/log.log', format='{time} {level} {message}', level='DEBUG')

parser = argparse.ArgumentParser()
parser.add_argument(
    '--url',
    type=str,
    default=None,
    nargs='+',
    help='Array of Links(urls) to resume. Default = None.'
)
args = parser.parse_args()

headers = {
    "User-Agent": "curl/7.64.1",
    "Accept": "*/*"
}

resume_data = defaultdict(list)

if __name__ == "__main__":
    urls = args.url
    for url in urls:
        logger.info(f"Принят URL: {url}\nДелаем запрос по заданному url...")
        try:
            response = requests.get(url, headers=headers)
        except Exception as err:
            logger.error(f"{type(err)}:\n{err}")
        else:
            resume_url = response.url
            resume_site = urlparse(resume_url).netloc
            logger.info(f"Запрос выполнен, статус ответа: {response.status_code}!")
            if 200 <= response.status_code <= 299:
                soup = BeautifulSoup(response.text, 'html.parser')
                logger.info("Начинаем парсить...")
                position = soup.findAll("h1", {"data-qa": "vacancy-title"})[0].text
                salary = soup.findAll("p", {"class": "vacancy-salary"})[0].text
                company_name = soup.findAll("a", {"class": "vacancy-company-name"})[0].text
                try:
                    place_company = soup.findAll("a", {"data-qa": "vacancy-view-link-location"})[0].text
                except Exception:
                    place_company = soup.findAll("p", {"data-qa": "vacancy-view-location"})[0].text
                logger.info(resume_site)
                resume_data["resume_site"].append(resume_site)
                logger.info(position)
                resume_data["position"].append(position)
                logger.info(salary)
                resume_data["salary"].append(salary)
                logger.info(resume_url)
                resume_data["resume_url"].append(resume_url)
                logger.info(company_name)
                resume_data["company_name"].append(company_name)
                logger.info(place_company)
                resume_data["place_company"].append(place_company)
            else:
                logger.error(f"Bad url: {resume_url}")

    frame = DataFrame(resume_data)
    print(tabulate(frame, headers='keys', tablefmt='psql'))
