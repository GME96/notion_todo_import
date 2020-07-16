from garminconnect import getHealthData
import json
from datetime import datetime, timedelta
print(datetime.today().weekday())


def setHealthDataToHabitTracker():
    # client = NotionClient(token)
    # cv = client.get_collection_view(url_habittracker)
    # for row in cv.collection.get_rows(search=today):
    #     if row.externalid == externalid:
    #         row.done = True
    response = getHealthData()
    dump = json.dumps(response)
    data = json.loads(dump)
    totalSteps = data['totalSteps']
    print(totalSteps)
    return totalSteps

print(setHealthDataToHabitTracker())
