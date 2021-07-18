"""
Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
"""
import requests
import json


openWeatherMapApiKey = "61ed2e188713dc956850cc34717ed3c8"  # ключ для атворизации
city = "Moscow"
countryCode = "RU"


URL = "http://api.openweathermap.org/data/2.5/weather"

params = {
    "q":  f"{city},{countryCode}",
    "APPID": openWeatherMapApiKey
}

headers = {
    'Content-Type': 'application/json',
    'cache-control': 'no-cache'
    }

req = requests.get(URL, params=params, headers=headers)
print(req.url)
print(req.status_code)
json_data = req.json()

with open('Moscow_weather.json', 'w') as f:  # сохраним данные в json файл
    json.dump(json_data, f)
