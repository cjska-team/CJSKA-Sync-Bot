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
        startTime = time.time()
        self.output("Sync loop started.")

        # TODO: Make the sync work!

        self.output("Sync loop finished.")
        endTime = time.time()
        self.output("Sync loop took approximately " + str(round(endTime - startTime, 2)) + " seconds")

    def runBot(self):
        self.output("SyncBot starting infinite loop.")
        while True:
            self.sync()

            self.output("Returning to idle state.")
            time.sleep(self.wait)
        self.output("Infinite loop terminated.")
