import requests

s_city = "Moscow,RU"
appid = ""

res = requests.get("http://api.openweathermap.org/data/2.5/weather",
             params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()

print("Город:", s_city)
print("Скорость ветра сейчас", data['wind']['speed'])
print("Видимость сейчас", data['visibility'], "\n\n")

res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                   params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()
print("Прогноз погоды на неделю:")
for i in data['list']:
    print("Дата <", i['dt_txt'],
     "> \r\nСкорость ветра <", i['wind']['speed'], ">",
     "> \r\nВидимость <", i['visibility'], ">")
    print("____________________________")
