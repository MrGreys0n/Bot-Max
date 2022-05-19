from tkinter import FIRST
from tokenize import group
import requests
import openpyxl
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

DAYS = {"понедельник": 0, "вторник": 1, "среда": 2, "четверг": 3,
        "пятница": 4, "суббота": 5, "воскресенье": 6}
FIRST_DAY = datetime(2022, 2, 7)

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

url = "https://www.mirea.ru/schedule/"
page = requests.get(url)
links = []
allLinks = []
soup = BeautifulSoup(page.text, "html.parser")
allLinks = soup.findAll('a', class_="uk-link-toggle")
for i in range(len(allLinks)):
    allLinks[i] = allLinks[i].get('href')
for link in allLinks:
    if 'ИИТ' in link and 'курс_21-22' in link:
        links.append(link)

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
#print(getDayOfWeek("Среда"))
#print(getEvenness())

# 7 нед (7 февраля) -- 1 неделя

#cell = sheet.cell(row = 2, column = 6).value

