"""
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
записывающую собранные вакансии в созданную БД.
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
"""
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from tabulate import tabulate  # для красивого вывода дата-фрейма
from pymongo import MongoClient

import argparse
from time import sleep
from collections import defaultdict
import csv
from pprint import pprint

from func import pars_salary
from mongo_func import mongo_update_without_duplicate

parser = argparse.ArgumentParser()
parser.add_argument(
    '--position',
    type=str,
    default=None,
    help='Position of interest. Default = None.'
)
parser.add_argument(
    '--page',
    type=int,
    default=1,
    help='Number of pages to parse. Default = 1.'
)
args = parser.parse_args()

headers = {
    "User-Agent": "curl/7.64.1",
    "Accept": "*/*"
}

root_url = "https://www.hh.ru/search/vacancy"
resume_site = "www.hh.ru"

resume_data = defaultdict(list)

client = MongoClient('localhost', 27017)
db = client['VacancyDB']
vacancy_collection = db['hh']

if __name__ == "__main__":
    position = args.position
    pages = args.page
    print(f"Position: {position}, page: {pages}.")

    params = {
        "area": f"",
        "APfromSearchLinePID": "true",
        "st": "searchVacancy",
        "text": position,
    }

    for page in range(0, pages):
        params["page"] = page
        response = requests.get(root_url, headers=headers, params=params)
        print(f"Принят URL: {response.url}\nДелаем запрос по заданному url...")
        print(f"Запрос выполнен, статус ответа: {response.status_code}!")
        if 200 <= response.status_code <= 299:
            soup = BeautifulSoup(response.text, 'html.parser')
            print("Начинаем парсить...")
            vacancies = soup.findAll("div", {"class": "vacancy-serp-item"})
            for vacancy in vacancies:
                resume_url = vacancy.findAll("a", {"data-qa": "vacancy-serp__vacancy-title"})[0]["href"]
                position = vacancy.findAll("a", {"data-qa": "vacancy-serp__vacancy-title"})[0].text
                salary = vacancy.findAll("div", {"class": "vacancy-serp-item__sidebar"})[0].text
                company_name = vacancy.findAll("a", {"data-qa": "vacancy-serp__vacancy-employer"})[0].text
                place_company = vacancy.findAll("span", {"data-qa": "vacancy-serp__vacancy-address"})[0].text
                min_salary, max_salary, currency = pars_salary(salary)
                resume_data["resume_site"].append(resume_site)
                resume_data["position"].append(position)
                resume_data["min_salary"].append(min_salary)
                resume_data["max_salary"].append(max_salary)
                resume_data["currency"].append(currency)
                resume_data["resume_url"].append(resume_url)
                resume_data["company_name"].append(company_name)
                resume_data["place_company"].append(place_company)
                # запись в монго
                mongo_dict = {
                    "resume_site": resume_site,
                    "position": position,
                    "min_salary": min_salary,
                    "max_salary": max_salary,
                    "currency": currency,
                    "resume_url": resume_url,
                    "company_name": company_name,
                    "place_company": place_company
                }

                # запись в монго
                mongo_update_without_duplicate(vacancy_collection, {"position": position, "company_name": company_name},
                                               {'$set': mongo_dict})
            # проверяем наличие кнопки дальше
            pages_ = list(map(lambda obj: obj.text, soup.findAll("a", {"data-qa": "pager-next"})))
            # print(pages_)
            if "дальше" not in pages_:
                print(f"Всего {page} страниц, задано было: {pages}.")
                break
        sleep(0.1)

    # вывод дата-фрейма в виде красивой таблицы
    frame = DataFrame(resume_data)
    print(tabulate(frame, headers='keys', tablefmt='psql'))

    # запись в csv
    with open('resume.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=list(resume_data.keys()))
        writer.writeheader()
        for i in range(len(resume_data["position"])):  # возьмем длину любого списка, так как теоретически они все равны
            writer.writerow({key: resume_data[key][i] for key in resume_data.keys()})

    # check
    # cursor = resume_collection.find({})
    # pprint(list(cursor))
    # cursor = resume_collection.find({})
    # print(len(list(cursor)))
