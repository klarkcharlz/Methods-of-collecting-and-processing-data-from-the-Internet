from pymongo import MongoClient

import argparse
from pprint import pprint

from mongo_func import find_interested_vacancy

parser = argparse.ArgumentParser()
parser.add_argument(
    '--salary',
    type=int,
    default=0,
    help='Salary of interest. Default = 0.'
)

args = parser.parse_args()

client = MongoClient('localhost', 27017)
db = client['VacancyDB']
vacancy_collection = db['hh']


if __name__ == "__main__":
    salary = args.salary
    vacancies = find_interested_vacancy(vacancy_collection, salary)
    pprint(vacancies)
    # print(len(vacancies))
