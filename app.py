
import os
from notion.client import NotionClient
from flask import Flask
from flask import request
import datetime
from datetime import datetime, timedelta


app = Flask(__name__)

url_habittracker = 'https://www.notion.so/c70b166df9834275b17ad3f54b0d7660?v=48e4b3434b794eb3a84805a649dce80f'
url_dokumente = 'https://www.notion.so/ba416195321d49448e79f501a7016d15?v=07e6e73352c845a3adbec2b3bbba698e'
url_kaufen = 'https://www.notion.so/17d4e68c0ffb4478a6ba2834211d69ee?v=09cf9854e500440aa54863637496ec3c'
url_todo = 'https://www.notion.so/1be6bd1ea4c9411e88f3f52dc05a4f7c?v=6e582135b0cc41889b459fccd40673d0'
url_tagesplan = 'https://www.notion.so/1cc58f95eeed473ca916efc14944c1ca?v=f9ad0cfd0bba413baf9361b401545dd8'
#today = date.today()

def createNotionTask(token, collectionURL, content, category, externalid, weekday):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.title = content
    row.category = category
    row.externalid = externalid
    row.Wochentag = weekday

def updateNotionTask(token, collectionURL, externalid):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    for row in cv.collection.get_rows(search=externalid):
        if row.externalid == externalid:
            row.done = True

def createNotionTaskFromCalender(token, collectionURL, content, externalid, duedate):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.title = content
    row.category = 'privat'
    row.externalid = externalid
    day = datetime.strptime(duedate[:10], '%Y-%m-%d')
    row.duedate = day
    row.source = 'calender'

def createEntryHabitTracker(token, date, string_date):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(url_habittracker)
    row = cv.collection.add_row()
    row.title = string_date
    row.date = date

def structureNotion(token):
    createEntryHabitTracker(token)

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
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createNotionTask(token_v2, url, todo, category, externalid, weekday)
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
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createNotionTaskFromCalender(token_v2, url, content, externalid, duedate)
    return f'added  in  to Notion!'

@app.route('/structureNotion', methods=['GET'])
def structureNotion():
    date = request.args.get('date')
    string_date = request.args.get('string_date')
    token_v2 = os.environ.get("TOKEN")
    createEntryHabitTracker(token_v2, date, string_date)
    return f'added  in  to Notion!'

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
