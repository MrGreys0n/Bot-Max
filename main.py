from tkinter import FIRST
from tokenize import group
import requests
import openpyxl
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


DAYS = {"понедельник": 0, "вторник": 1, "среда": 2, "четверг": 3,
        "пятница": 4, "суббота": 5, "воскресенье": 6}
FIRST_DAY = datetime(2022, 2, 7)
WEATHER_KEY = '0f9e28e70c3287577404f914752dc92d'
URL = "https://www.mirea.ru/schedule/"


def getDayOfWeek(day):
    if day.lower() == "сегодня":
        dow = int(datetime.today().weekday())
    elif day.lower() == "завтра":
        dow = (int(datetime.today().weekday()) + 1) % 7
    else:
        dow = DAYS[day.lower()]
    return dow

def getEvenness(day = datetime.today()):
    if day == 'сегодня':
        day = datetime.today()
    elif day == 'завтра':
        day = datetime.today() + timedelta(1)
    week = ((int((day - FIRST_DAY).days)) // 7) % 7 + 1
    if week == 0:
        return 1
    return 0

def getSchedule(group, day, evenness=0):
    schedule = []
    if day == 6:
        return 
    for i in range(1, num_cols):
        if sheet.cell(2, i).value == group:
            for s in range(4 + 12 * day + evenness, 4 + 12 * (day + 1) + evenness, 2):
                subj = sheet.cell(s, i).value
                schedule.append(subj) if subj else schedule.append("---")
    return schedule

def getLinks():
    page = requests.get(URL)
    links = []
    allLinks = []
    soup = BeautifulSoup(page.text, "html.parser")
    allLinks = soup.findAll('a', class_="uk-link-toggle")
    for i in range(len(allLinks)):
        allLinks[i] = allLinks[i].get('href')
    for link in allLinks:
        if 'ИИТ' in link and 'курс_21-22' in link:
            links.append(link)
    return links


weathet_url = "http://api.openweathermap.org/data/2.5/weather?q=moscow&appid=a" + WEATHER_KEY + "a&units=metric"
response = requests.get(weathet_url)
info = response.json()
print(info)
temp = info["main"]["temp"]

'''



curlink = links[0]
f = open("c:/Users/serge/Desktop/file.xlsx", "wb")
resp = requests.get(curlink)
f.write(resp.content)
f.close()

book = openpyxl.load_workbook("c:/Users/serge/Desktop/file.xlsx") # открытие файла
sheet = book.active # активный лист
num_cols = sheet.max_column # количество столбцов
num_rows = sheet.max_row # количество строк

group = "ИКБО-08-21"
day = "пятница"

if day.lower() not in ("сегодня", "завтра"):
    day = getDayOfWeek(day)
    print("Расписание для нечетной недели:")
    schedule = getSchedule(group, day, 0)
    for i in range(len(schedule)):
        print(str(i+1) + "  " + schedule[i])
    print("_____________________________")
    print("Расписание для четной недели:")
    schedule = getSchedule(group, day, 1)
    for i in range(len(schedule)):
        print(str(i+1) + "  " + schedule[i])
else:    
    ev = getEvenness(day)
    day = getDayOfWeek(day)
    print(getSchedule(group, day, ev))


def main():
    vk_session = vk_api.VkApi(token='0021cf58bb0d25bd735c01918b092284fa1f13be6e3943558152c8c4a1299c9c7895bb569a308481ee3c8')
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Красная кнопка', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line() # переход на вторую строку
    keyboard.add_button('Зелёная кнопка', color=VkKeyboardColor.POSITIVE)
    
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.text and event.to_me:
            print('New from {}, text = {}'.format(event.user_id, event.text))
            vk.messages.send(
                user_id = event.user_id,
                random_id = get_random_id(),
                message = 'Привет, ' + \
                vk.users.get(user_id = event.user_id)[0]['first_name']
            )
            vk.messages.send(
                user_id = event.user_id,
                random_id = get_random_id(),
                keyboard=keyboard.get_keyboard(),
                message='Пример клавиатуры'
            )

if __name__ == '__main__':
    main()
'''
#print(getDayOfWeek("Среда"))
#print(getEvenness())

# 7 нед (7 февраля) -- 1 неделя

#cell = sheet.cell(row = 2, column = 6).value

