"""
Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.
"""
import requests
import json


USER = "klarkcharlz"
URL = f"https://api.github.com/users/{USER}/repos"

req = requests.get(URL)
print(req.status_code)

json_data = req.json()
repos = [d["name"] for d in json_data]
print(repos)  # отобразим список названий репозиториев

with open('user_repos.json', 'w') as f:  # сохраним полные данные в json файл
    json.dump(json_data, f)
