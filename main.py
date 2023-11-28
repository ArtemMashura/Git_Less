import requests as requests
from bs4 import BeautifulSoup

#С сайта погоды вывести температуру на 7 дней вперед
#https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%B4%D0%BD%D0%B5%D0%BF%D1%80-303007131

url = 'https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%B4%D0%BD%D0%B5%D0%BF%D1%80-303007131'
htmlPage = requests.get(url)

weather_7day = {}
# day = {
#     'number'
#     'dayWeek'
#     'month'
#     'min'
#     'max' }


def get_7day(html):
    w7day = {}
    class_tab = 'tabs' # блок HTML с перечнем 7 дней и прогнозом на них

    html_7day = html.find('div', class_=class_tab)
    i = 0

    for html_day in html_7day.find_all('div', 'main'):
        i = i + 1
        w1day = {}
        day_link = html_day.find(['p', 'a'], class_='day-link')
        if day_link:
            w1day.update({"dayWeek": str(day_link.text)})
        date = html_day.find('p', class_='date')
        if date:
            w1day.update({"number": str(date.text)})
        month = html_day.find('p', class_='month')
        if month:
            w1day.update({"month": str(month.text)})

        html_temperature = html_day.find('div', class_='temperature')
        min_temp = html_temperature.find('span')

        max_temp = min_temp.findNext('span')

        if min_temp and max_temp:
            w1day.update({"min": str(min_temp.text)})
            w1day.update({"max": str(max_temp.text)})

        w7day.update({i: w1day})

    return w7day


def print_w7day(w7day):
    print("Прогноз погоды на семь дней")
    for day in w7day.values():
        print(day['dayWeek'], '(', day['number'], ' ', day['month'], '): min = ', day['min'], ' | max = ', day['max'])


if htmlPage.status_code == 200:
    soup = BeautifulSoup(htmlPage.text, 'html.parser')
    weather_7day = get_7day(soup)

    print_w7day(weather_7day)
else:
    print('not 200')

print('POGODA ')