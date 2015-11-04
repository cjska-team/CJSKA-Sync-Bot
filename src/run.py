import sys
import time
from firebase_token_generator import create_token
from bot import SyncBot

waitTime = (60 * 1)
logFileLoc = "./output/"

def getFirebaseToken(secret, uid):
    return create_token(secret, {
        "uid": uid
    },
    {
        "admin": True
    })

print("Command Line arguments: " + str(sys.argv))
try:
    fbSecret = str(sys.argv[1])
    fbUserID = str(sys.argv[2])

    if fbSecret != "MY_FIREBASE_SECRET" and fbUserID != "MY_FIREBASE_UID":
        fbToken = getFirebaseToken(fbSecret, fbUserID)

        botInstance = SyncBot(fbToken, waitTime, logFileLoc)

        botInstance.runBot()
    else:
        print("Uh-oh! It looks like you forgot to include a valid Firebase Secret and/or a valid Firebase UID.")
except IndexError:
    print("Sorry, we couldn't find the correct command line argument. Exiting!")
