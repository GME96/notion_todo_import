
import os
from notion.client import NotionClient
from flask import Flask
from flask import request
from datetime import datetime, timedelta


app = Flask(__name__)


def createNotionTask(token, collectionURL, content, category, externalid):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.title = content
    row.category = category
    row.externalid = externalid

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

# def structureToDo(token, collectionURL, startdate, enddate):
#     # notion
#     client = NotionClient(token)
#     cv = client.get_collection_view(collectionURL)
#     for row in cv.collection.get_rows():
#         if row.duedate != None:
#             if startdate < row.duedate < enddate and row.done is False and row.Wochentag = None:
#                 row.done = True



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
        category = ''
    externalid = request.args.get('externalid')
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createNotionTask(token_v2, url, todo, category, externalid)
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

# @app.route('/structureToDo', methods=['GET'])
# def create_todo_calender():
#
#     content = request.args.get('content')
#     duedate = request.args.get('duedate')
#     externalid = request.args.get('externalid')
#     token_v2 = os.environ.get("TOKEN")
#     url = os.environ.get("URL")
#     createNotionTaskFromCalender(token_v2, url, content, externalid, duedate)
#     return f'added  in  to Notion!'

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
