
import os
from notion.client import NotionClient
from flask import Flask
from flask import request
import datetime
from datetime import datetime, timedelta
#from garminconnect import getHealthData
import json


app = Flask(__name__)

url_habittracker = 'https://www.notion.so/c70b166df9834275b17ad3f54b0d7660?v=48e4b3434b794eb3a84805a649dce80f'
url_dokumente = 'https://www.notion.so/ba416195321d49448e79f501a7016d15?v=07e6e73352c845a3adbec2b3bbba698e'
url_kaufen = 'https://www.notion.so/17d4e68c0ffb4478a6ba2834211d69ee?v=09cf9854e500440aa54863637496ec3c'
url_todo = 'https://www.notion.so/1be6bd1ea4c9411e88f3f52dc05a4f7c?v=6e582135b0cc41889b459fccd40673d0'
url_tagesplan = 'https://www.notion.so/1cc58f95eeed473ca916efc14944c1ca?v=f9ad0cfd0bba413baf9361b401545dd8'
url_weekly = 'https://www.notion.so/2daabbf4909b4ba6aa5033bd4f1f979f?v=01d0e7de43874af0b224b02be0209456'
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
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.title = (duedate[11:16] + ' ' + content)
    row.category = 'privat'
    row.externalid = externalid
    day = datetime.strptime(duedate[:10], '%Y-%m-%d')
    row.duedate = day
    row.executionDate = datetime.strptime(executionDate[:10], '%Y-%m-%d')
    row.source = 'calender'

def createEntryHabitTracker(token, date, string_date):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(url_habittracker)
    row = cv.collection.add_row()
    row.title = date[9:10]
    row.date = date.strptime(date[:10], '%Y-%m-%d')

def createEntryWeeklyPlanner(token, date):
    client = NotionClient(token)
    cv = client.get_collection_view(url_weekly)
    row = cv.collection.add_row()
    startdate =  date.strptime(date[:10], '%Y-%m-%d')
    enddate = startdate + timedelta(days=7)
    enddatestring = enddate.strftime("%d")
    title_text = date[9:10]  + ' - ' + enddatestring + '.' +  date[6:7] + '.' + date[0:4] ##convert bis date properly
    row.title = title_text
    row.startdate = startdate
    row.enddate = enddate

def sortTask(token):
    client = NotionClient(token)
    cv = client.get_collection_view(url_todo)
    for row in cv.collection.get_rows(search=''):
        if row.done == False:
            if row.executionDate.weekday() == 0:
                row.Wochentag = 'Monday'
            elif row.executionDate.weekday() == 1:
                row.Wochentag = 'Tuesday'
            elif row.executionDate.weekday() == 2:
                row.Wochentag = 'Wednesday'
            elif row.executionDate.weekday() == 3:
                row.Wochentag = 'Thursday'
            elif row.executionDate.weekday() == 4:
                row.Wochentag = 'Friday'
            elif row.executionDate.weekday() == 5:
                row.Wochentag = 'Saturday'
            elif row.executionDate.weekday() == 6:
                row.Wochentag = 'Sunday'



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
    createEntryHabitTracker(token, date, string_date)
    sortTask(token)
    if datetime.today().weekday() == 0
        createEntryWeeklyPlanner(token, date)

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

@app.route('/structureNotionDay', methods=['GET'])
def structureNotionDay():
    date = request.args.get('date')
    string_date = request.args.get('string_date')
    token_v2 = os.environ.get("TOKEN")
    structureNotion(token_v2, date, string_date)
    return f'added  in  to Notion!'

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
