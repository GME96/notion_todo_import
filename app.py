
import os
from notion.client import NotionClient
from flask import Flask
from flask import request
import datetime
from datetime import datetime, timedelta, date
#from garminconnect import getHealthData
import json


app = Flask(__name__)

url_habittracker = 'https://www.notion.so/c70b166df9834275b17ad3f54b0d7660?v=48e4b3434b794eb3a84805a649dce80f'
url_dokumente = 'https://www.notion.so/ba416195321d49448e79f501a7016d15?v=07e6e73352c845a3adbec2b3bbba698e'
url_kaufen = 'https://www.notion.so/17d4e68c0ffb4478a6ba2834211d69ee?v=09cf9854e500440aa54863637496ec3c'
url_todo = 'https://www.notion.so/1be6bd1ea4c9411e88f3f52dc05a4f7c?v=6e582135b0cc41889b459fccd40673d0'
url_tagesplan = 'https://www.notion.so/1cc58f95eeed473ca916efc14944c1ca?v=f9ad0cfd0bba413baf9361b401545dd8'
url_weekly = 'https://www.notion.so/2daabbf4909b4ba6aa5033bd4f1f979f?v=01d0e7de43874af0b224b02be0209456'
url_month = 'https://www.notion.so/11ccde35d54449c9a41938960f3bb996?v=78b0d3bbc28946f8acaa002210a16ec4'
url_impfungen = 'https://www.notion.so/4d70f923f8944bb49737cf90ce675839?v=8910c7d5bf6341339aeb83ec0a531aa3'
url_calender = 'https://www.notion.so/8ed763fd1835430791484321a0d40a44?v=eaaa5067b942495692ad6c9aa3532870'
url_kalender_sync = 'https://www.notion.so/3661b0a791d54578960a63052428ab28?v=7d63056f24a64bf0a3c89495735131e8'
url_freunde = 'https://www.notion.so/76bc0c7f21ef40b6a64ec1e7ab712555?v=335a5d037ca54b3aae64731031adaa7e'
url_goals = 'https://www.notion.so/411fdf381a154f8fbed55749df7b18bd?v=6ac7c0cbb2734110be173d9cb220ac72'
#today = date.today()

def createNotionTask(token, collectionURL, content, category, externalid, weekday, executionDate):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.title = content
    row.category = category
    row.externalid = externalid
    row.Wochentag = weekday
    row.executionDate = datetime.strptime(executionDate[:10], '%Y-%m-%d')

def updateNotionTask(token, collectionURL, externalid):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    for row in cv.collection.get_rows(search=externalid):
        if row.externalid == externalid:
            row.done = True

def createNotionTaskFromCalender(token, collectionURL, content, externalid, duedate, executionDate):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(url_kalender_sync)
    row = cv.collection.add_row()
    row.name = (duedate[11:16] + ' ' + content)
    row.category = 'privat'
    row.externalid = externalid
    day = datetime.strptime(duedate[:10], '%Y-%m-%d')
    row.duedate = day
    row.executionDate = datetime.strptime(executionDate[:10], '%Y-%m-%d')
    row.source = 'calender'

def createEntryHabitTracker(token, day, string_date, week, weekday):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(url_habittracker)
    goals = client.get_collection_view(url_goals)
    row = cv.collection.add_row()
    datetimeobj = datetime.strptime(day[:10], '%Y-%m-%d')
    row.title = datetimeobj.strftime("%d") + '.' +  datetimeobj.strftime("%m") + '.' + datetimeobj.strftime("%Y")
    row.date = datetimeobj
    row.week = week
    row.Wochentag = weekday
    for goal in goals.collection.get_rows(search=''):
        startdate = goal.startdate.start
        duedate =  goal.duedate.start
        if startdate <= datetimeobj.date() <= duedate:
            row.goals = goals

def createEntryWeeklyPlanner(token):
    client = NotionClient(token)
    cv = client.get_collection_view(url_weekly)
    row = cv.collection.add_row()
    startdate = date.today() + timedelta(days=1)
    enddate = startdate + timedelta(days=6)
    title_text = startdate.strftime("%d") + '.' +  startdate.strftime("%m") + ' - ' + enddate.strftime("%d") + '.' +  enddate.strftime("%m") + '.' + enddate.strftime("%Y")
    row.title = title_text
    row.startdate = startdate
    row.enddate = enddate
    createDailyEntryInHabitTrackerForOneWeek(token, startdate, row)

# def createNewMonth(token, startdate):
#     client = NotionClient(token)
#     cv = client.get_collection_view(url_month)
#     token = token
#     month_int = date.today().month
#     if month_int == 1:
#         month = 'Jänner'
#     elif month_int == 2:
#         month = 'Februar'
#     elif month_int == 3:
#         month = 'März'
#     elif month_int == 4:
#         month = 'April'
#     elif month_int == 5:
#         month = 'Mai'
#     elif month_int == 6:
#         month = 'Juni'
#     elif month_int == 7:
#         month = 'Juli'
#     elif month_int == 8:
#         month = 'August'
#     elif month_int == 9:
#         month = 'September'
#     elif month_int == 10:
#         month = 'Oktober'
#     elif month_int == 11:
#         month = 'November'
#     elif month_int == 12:
#         month = 'Dezember'
#     row.title = month + ' ' + startdate.strftime("%Y")

def createDailyEntryInHabitTrackerForOneWeek(token, startdate, week):
    client = NotionClient(token)
    cv = client.get_collection_view(url_habittracker)
    token = token
    for x in range(7):
        date = startdate + timedelta(days=x)
        stringdate = date.strftime('%Y-%m-%d')
        if x == 0:
            weekday = 'Montag'
        elif x == 1:
            weekday = 'Dienstag'
        elif x == 2:
            weekday = 'Mittwoch'
        elif x == 3:
            weekday = 'Donnerstag'
        elif x == 4:
            weekday = 'Freitag'
        elif x == 5:
            weekday = 'Samstag'
        elif x == 6:
            weekday = 'Sonntag'
        createEntryHabitTracker(token, stringdate, '', week, weekday)

def sortTask(token):
    client = NotionClient(token)
    cv = client.get_collection_view(url_todo)
    for row in cv.collection.get_rows(search=''):
        if row.done == False:
            row.executionDate
            # if row.executionDate.weekday() == 0:
            #     row.Wochentag = 'Monday'
            # elif row.executionDate.weekday() == 1:
            #     row.Wochentag = 'Tuesday'
            # elif row.executionDate.weekday() == 2:
            #     row.Wochentag = 'Wednesday'
            # elif row.executionDate.weekday() == 3:
            #     row.Wochentag = 'Thursday'
            # elif row.executionDate.weekday() == 4:
            #     row.Wochentag = 'Friday'
            # elif row.executionDate.weekday() == 5:
            #     row.Wochentag = 'Saturday'
            # elif row.executionDate.weekday() == 6:
            #     row.Wochentag = 'Sunday'



# def setHealthDataToHabitTracker():
#     # client = NotionClient(token)
#     # cv = client.get_collection_view(url_habittracker)
#     # for row in cv.collection.get_rows(search=today):
#     #     if row.externalid == externalid:
#     #         row.done = True
#     response = getHealthData()
#     dump = json.dumps(response)
#     data = json.loads(dump)
#     totalSteps = data['totalSteps']
#     print(totalSteps)
#     return totalSteps

def structureNotion(token, date, string_date):
    sortTask(token)

def OnSundayEvening(token):
    createEntryWeeklyPlanner(token)


def updateCalender(token):
    client = NotionClient(token)
    calender = client.get_collection_view(url_calender)
    impfungen = client.get_collection_view(url_impfungen)
    kalender = client.get_collection_view(url_kalender_sync)
    todo = client.get_collection_view(url_todo)
    freunde = client.get_collection_view(url_freunde)
    for impfung in impfungen.collection.get_rows(search=''):
        if impfung.exportedToCalender == False:
            calenderEntry = calender.collection.add_row()
            calenderEntry.name = impfung.name
            calenderEntry.type = 'Impfungen'
            impfung.calender = calenderEntry
            impfung.exportedToCalender = True
    for to in todo.collection.get_rows(search=''):
        if to.exportedToCalender == False:
            calenderEntry = calender.collection.add_row()
            calenderEntry.name = to.name
            calenderEntry.type = 'ToDo'
            to.calender = calenderEntry
            to.exportedToCalender = True
    for eintrag in calender.collection.get_rows(search=''):
        if eintrag.exportedToCalender == False:
            calenderEntry = calender.collection.add_row()
            calenderEntry.name = eintrag.name
            calenderEntry.type = 'Kalender'
            eintrag.calender = calenderEntry
            eintrag.exportedToCalender = True
    for person in freunde.collection.get_rows(search=''):
        if person.exportedToCalender == False:
            calenderEntry = calender.collection.add_row()
            calenderEntry.name = person.name
            calenderEntry.type = 'Geburtstag'
            person.calender = calenderEntry
            person.exportedToCalender = True




@app.route('/create_todo', methods=['GET'])
def create_todo():

    todo = request.args.get('todo')
    parentID = request.args.get('parentID')
    if parentID == 'AQMkADAwATYwMAItZDg4ADQtZTM0YS0wMAItMDAKAC4AAAPNUpFw5pxeQqiq0XlCNIkkAQCILp6LM0zpSYe2oI3McKECAANLdDYDAAAA':
        category = 'privat'
    elif parentID == 'AQMkADAwATYwMAItZDg4ADQtZTM0YS0wMAItMDAKAC4AAAPNUpFw5pxeQqiq0XlCNIkkAQCILp6LM0zpSYe2oI3McKECAANLdDX7AAAA':
        category = 'privat'
    elif parentID == 'AQMkADAwATYwMAItZDg4ADQtZTM0YS0wMAItMDAKAC4AAAPNUpFw5pxeQqiq0XlCNIkkAQCILp6LM0zpSYe2oI3McKECAANLdDX6AAAA':
        category = 'master'
    elif parentID == 'AQMkADAwATYwMAItZDg4ADQtZTM0YS0wMAItMDAKAC4AAAPNUpFw5pxeQqiq0XlCNIkkAQCILp6LM0zpSYe2oI3McKECAANLdDX4AAAA':
        category = 'masterarbeit'
    elif parentID == 'AQMkADAwATYwMAItZDg4ADQtZTM0YS0wMAItMDAKAC4AAAPNUpFw5pxeQqiq0XlCNIkkAQCILp6LM0zpSYe2oI3McKECAANLdDX9AAAA':
        category = 'transport'
    elif parentID == 'AQMkADAwATYwMAItZDg4ADQtZTM0YS0wMAItMDAKAC4AAAPNUpFw5pxeQqiq0XlCNIkkAQCILp6LM0zpSYe2oI3McKECAANLdDYAAAE=':
        category = 'transport'
    elif parentID == 'AQMkADAwATYwMAItZDg4ADQtZTM0YS0wMAItMDAKAC4AAAPNUpFw5pxeQqiq0XlCNIkkAQCILp6LM0zpSYe2oI3McKECAANLdDX-AAAA':
        category = 'wohnung'
    else:
        category = request.args.get('category')

    externalid = request.args.get('externalid')
    weekday = request.args.get('weekday')
    executionDate = request.args.get('executionDate')
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createNotionTask(token_v2, url, todo, category, externalid, weekday, executionDate)
    return f'added {todo} in {category} to Notion!'

@app.route('/update_todo', methods=['GET'])
def update_todo():

    externalid = request.args.get('externalid')
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    updateNotionTask(token_v2, url, externalid)
    return f'checked set done to Notion!'

@app.route('/create_todo_calender', methods=['GET'])
def create_todo_calender():

    content = request.args.get('content')
    duedate = request.args.get('duedate')
    externalid = request.args.get('externalid')
    executionDate = request.args.get('executionDate')
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createNotionTaskFromCalender(token_v2, url, content, externalid, duedate, executionDate)
    return f'added  in  to Notion!'

@app.route('/updateCalender', methods=['GET'])
def CallupdateCalender():
    token_v2 = os.environ.get("TOKEN")
    updateCalender(token_v2)
    return f'Calender was updated'

@app.route('/structureNotionDay', methods=['GET'])
def structureNotionDay():
    date = request.args.get('date')
    string_date = request.args.get('string_date')
    token_v2 = os.environ.get("TOKEN")
    structureNotion(token_v2, date, string_date)
    return f'added  in  to Notion!'

@app.route('/CallOnSundayEvening', methods=['GET'])
def CallOnSundayEvening():
    token_v2 = os.environ.get("TOKEN")
    OnSundayEvening(token_v2)
    return f'added  in  to Notion!'

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
