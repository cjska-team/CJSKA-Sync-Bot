import sys
import requests
import json
import time
from ka_api import KA_API
from firebase_token_generator import create_token

kaApiWrapper = KA_API()

class SyncBot:
    def __init__(self, firebaseToken, pauseTime, logFileLoc):
        self.wait = pauseTime
        self.logFile = open(logFileLoc, "w")

        self.output("SyncBot initialized")

    def output(self, msg):
        print("[LOG] (" + str(time.ctime()) + ") - " + str(msg))
        self.logFile.write("[" + str(time.ctime()) + "] - " + msg + "\n")

    def sync(self):
        self.output("Sync loop started.")
        # TODO: Make the sync work!
        self.output("Sync loop finished.")

    def runBot(self):
        self.output("SyncBot starting infinite loop.")
        while True:
            self.sync()

            self.output("Returning to idle state.")
            time.sleep(self.wait)
        self.output("Infinite loop terminated.")

# def main(firebaseSecret, firebaseUID):
#     output("New bot instance started!")
#     if firebaseSecret != "MY_FIREBASE_SECRET" and firebaseUID != "MY_FIREBASE_UID":
#         fbToken = getFirebaseToken(firebaseSecret, firebaseUID)
#
#         print("Begin wait")
#         sleep(10)
#         print("Done")
#     else:
#         print("Uh-oh! It looks like you forgot to include a valid Firebase Secret and/or a valid Firebase UID.")
#         return
