import sys
import requests
import json
import time

class Bot:
    def __init__(self, username, password, interval):
        self.username = username
        self.password = password
        self.interval = interval
        self.logLocation = "./output/" + str(time.ctime()).replace(" ", "-") + ".txt"
        self.logFile = open(self.logLocation, "w")
        self.authenticated = False
        self.authenticate()

        self.appId = "F4jHkOZFPQTGPZ23D1CqaNxmbLqoAUAxBzcnlWQn"
        self.apiKey = "y2Zb0XAzVCHz8wkH8eiQPaFtk7yGK3Yzm0mPDNmW"

        self.generalRequestHeaders = {
            "X-Parse-Application-Id": "F4jHkOZFPQTGPZ23D1CqaNxmbLqoAUAxBzcnlWQn",
            "X-Parse-REST-API-Key": "y2Zb0XAzVCHz8wkH8eiQPaFtk7yGK3Yzm0mPDNmW"
        }

    def logMsg(self, msg):
        currTime = str(time.ctime())
        logMsg = "(" + currTime + ") " + msg + "\n"
        print(logMsg)
        self.logFile.write(logMsg)

    def authenticate(self):
        urlParams = {
            "username": self.username,
            "password": self.password
        }
        reqHeaders = {
            "X-Parse-Application-Id": "F4jHkOZFPQTGPZ23D1CqaNxmbLqoAUAxBzcnlWQn",
            "X-Parse-REST-API-Key": "y2Zb0XAzVCHz8wkH8eiQPaFtk7yGK3Yzm0mPDNmW",
            "X-Parse-Revocable-Session": "1"
        }
        request = requests.get("https://api.parse.com/1/login", params=urlParams, headers=reqHeaders)

        if request.status_code == 200:
            self.authenticated = True

    def getStoredContests(self):
        request = requests.get("https://api.parse.com/1/classes/Contest", headers=self.generalRequestHeaders)

        print(request.json())

    def getStoredEntriesForContest(self, contestId):
        urlParams = {
            "where": json.dumps({
                "contestId": str(contestId)
            })
        }
        request = requests.get("https://api.parse.com/1/classes/Entry", params=urlParams, headers=self.generalRequestHeaders)

        print(request.json())

    def run(self):
        self.logMsg("Bot loop spinning up")
        while True:
            if self.authenticated == True:
                self.sync()
            else:
                self.logMsg("Bot not authenticated!")

            self.logMsg("Bot returning to idle state")
            time.sleep(self.interval)

        self.logMsg("Bot loop terminated")

    def sync(self):
        self.getStoredContests()
        self.getStoredEntriesForContest("0000")