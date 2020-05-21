
import os
from notion.client import NotionClient
from flask import Flask
from flask import request


app = Flask(__name__)


def createNotionTask(token, collectionURL, content, category, externalid):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.title = content
    row.category = category
    row.externalid = externalid


@app.route('/create_todo', methods=['GET'])
def create_todo():

    todo = request.args.get('todo')
    parentID = request.args.get('parentID')
    if parentID == 'AQMkADAwATYwMAItZDg4ADQtZTM0YS0wMAItMDAKAC4AAAPNUpFw5pxeQqiq0XlCNIkkAQCILp6LM0zpSYe2oI3McKECAANLdDYDAAAA':
        category = 'privat'
    elif parentID == '2':
        category = 'master'
    elif parentID == '3':
        category = 'masterarbeit'
    elif parentID == '4':
        category = 'transport'
    elif parentID == '5':
        category = 'transport'
    else:
        category = ''
    externalid = request.args.get('externalid')
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createNotionTask(token_v2, url, todo, category, externalID)
    return f'added {todo} to Notion'


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
