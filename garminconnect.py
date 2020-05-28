
#!/usr/bin/env python3

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)
import json
from datetime import date
today = date.today()

def initiaConnection():
    try:

        Garmin_User = os.environ.get("Garmin_User")
        Garmin_Passwort = os.environ.get("Garmin_Passwort")
        client = Garmin(Gamrin_User, Garmin_Passwort)
    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        print("Error occured during Garmin Connect Client init: %s" % err)
        quit()
    except Exception:  # pylint: disable=broad-except
        print("Unknown error occured during Garmin Connect Client init")
        quit()

    """
    Login to Garmin Connect portal
    Only needed at start of your program
    The libary will try to relogin when session expires
    """
    try:
        client.login()
    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        print("Error occured during Garmin Connect Client login: %s" % err)
        quit()
    except Exception:  # pylint: disable=broad-except
        print("Unknown error occured during Garmin Connect Client login")
        quit()

    return client


def getHealthData():
    client = initiaConnection()
    response = client.get_stats(today.isoformat())
    return response
    print(getHealthData())
