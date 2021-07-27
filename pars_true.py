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
from pandas import DataFrame
from tabulate import tabulate  # для красивого вывода дата-фрейма

import argparse
from time import sleep
from collections import defaultdict
import csv

from func import pars_salary


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
                resume_data["salary"].append(salary)
                resume_data["resume_url"].append(resume_url)
                resume_data["company_name"].append(company_name)
                resume_data["place_company"].append(place_company)
        sleep(0.2)

    # вывод дата-фрейма в виде красивой таблицы
    frame = DataFrame(resume_data)
    print(tabulate(frame, headers='keys', tablefmt='psql'))

    with open('resume.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=list(resume_data.keys()))
        writer.writeheader()
        for i in range(len(resume_data["position"])):  # возьмем длину любого списка, так как теоретически они все равны
            writer.writerow({key: resume_data[key][i] for key in resume_data.keys()})
