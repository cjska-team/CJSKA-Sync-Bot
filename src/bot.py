import sys
import requests
import json
import time
from ka_api import KA_API
from firebase_token_generator import create_token

kaApiWrapper = KA_API()

class SyncBot:
    def __init__(self, firebaseToken, pauseTime, logFileLoc):
        self.firebaseToken = firebaseToken
        self.wait = pauseTime
        self.logFile = open(logFileLoc + "log_" + str(time.ctime()).replace(" ", "-") + ".txt", "w")
        self.firebaseApp = "https://contest-judging-sys.firebaseio.com"
        print("Firebase token: " + self.firebaseToken)
        self.output("SyncBot initialized")

    def output(self, msg, prefix="Sync  Bot"):
        currTime = str(time.ctime())
        print("(" + currTime + ") [" + prefix + "] - " + str(msg))
        self.logFile.write("(" + currTime + ") [" + prefix + "] - " + msg + "\n")

    def getStoredContests(self):
        apiRequest = requests.get(self.firebaseApp + "/contestKeys.json?print=pretty")
        responseJSON = apiRequest.json()

        if responseJSON == None:
            return {}
        else:
            return responseJSON

    def getStoredContestEntries(self, contestId):
        apiRequest = requests.get(self.firebaseApp + "/contests/" + str(contestId) + "/entryKeys.json?print=pretty")
        responseJSON = apiRequest.json()

        if responseJSON == None:
            return {}
        else:
            return responseJSON

    def sync(self):
        startTime = time.time()
        self.output("Sync Loop Started")

        self.output("Fetching contest programs from Khan Academy", "DiffCheck")
        kaContests = kaApiWrapper.getContests()

        self.output("Fetching contests stored in Firebase", "DiffCheck")
        fbContests = self.getStoredContests()

        newKAContests = {} # Contests to add to Firebase
        delKAContests = [] # Contests to delete from Firebase

        newKAContestEntries = {} # Contests Entries to add to Firebase
        delKAContestEntries = {} # Contest Entries to delete from Firebase

        # Phase 1: Check for new data
        self.output("Beginning Sync Phase 1 (Checking for new content)", "DiffCheck")
        for kaContest in kaContests:
            if kaContest in fbContests:
                # Check for new contest entries
                # ...

                newKAContestEntries[str(kaContest)] = {}

                self.output("Fetching contest entries from Khan Academy (for contest with ID " + kaContest + ")", "DiffCheck")
                kaContestEntries = kaApiWrapper.getContestEntries(kaContest)

                self.output("Fetching contest entries stored in Firebase (for contest with ID " + kaContest + ")", "DiffCheck")
                fbContestEntries = self.getStoredContestEntries(kaContest)

                for kaContestEntry in kaContestEntries:
                    if kaContestEntry in fbContestEntries:
                        pass
                    else:
                        self.output("Untracked contest entry found. Contest ID: " + str(kaContest) + " Entry ID: " + str(kaContestEntry), "DiffCheck")
                        newKAContestEntries[str(kaContest)][str(kaContestEntry)] = kaContestEntries[kaContestEntry]
            else:
                self.output("Untracked contest found. ID: " + str(kaContest), "DiffCheck")
                newKAContests[str(kaContest)] = kaContests[kaContest]
                # kaContestsAdded.append(str(kaContest))

        # Phase 2: Check for deleted data
        self.output("Beginning Sync Phase 2 (Checking for deleted content)", "DiffCheck")
        for fbContest in fbContests:
            if fbContest in kaContests:
                # Check for deleted contest entries
                # ...

                delKAContestEntries[str(fbContest)] = []

                self.output("Fetching contest entries from Khan Academy (for contest with ID " + fbContest + ")", "DiffCheck")
                kaContestEntries = kaApiWrapper.getContestEntries(fbContest)

                self.output("Fetching contest entries stored in Firebase (for contest with ID " + fbContest + ")", "DiffCheck")
                fbContestEntries = self.getStoredContestEntries(fbContest)

                for fbContestEntry in fbContestEntries:
                    if fbContestEntry in kaContestEntries:
                        pass
                    else:
                        self.output("Found a contest entry that no longer exists. Contest ID: " + str(fbContest) + " Entry ID: " + str(fbContestEntry), "DiffCheck")
                        delKAContestEntries[str(fbContest)].append(str(fbContestEntry))
            else:
                self.output("Found a contest that no longer exists. ID: " + str(fbContest), "DiffCheck")
                delKAContests.append(str(fbContest))

        # self.output("Untracked contests: " + str(newKAContests), "DiffDebug")
        # self.output("Contests with untracked entries: " + str(newKAContestEntries), "DiffDebug")

        # Phase 3: Write new data
        # TODO: Push the actual scratchpad data to Firebase!
        # P3A: Write new contests
        for newContest in newKAContests:
            # For some reason, the following PUT request continues to return HTTP 401 (AKA unauthorized)
            addContestReq = requests.put(self.firebaseApp + "/contests/" + str(newContest) + "/.json?auth=" + str(self.firebaseToken), data=json.dumps(newKAContests[newContest]), headers={"content-type": "application/json"})
            if addContestReq.status_code == 200:
                requests.put(self.firebaseApp + "/contestKeys/" + str(newContest) + "/.json?auth=" + str(self.firebaseToken), data="true")
            else:
               self.output("PUT Request to Firebase failed while trying to push new contests. Status Code: " + str(addContestReq.status_code), "FATAL")

        # P3B: Write new contest entries
        for contestWithNewEntries in newKAContestEntries:
            for newContestEntry in newKAContestEntries[contestWithNewEntries]:
                addEntryReq = requests.put(self.firebaseApp + "/contests/" + str(contestWithNewEntries) + "/entries/" + str(newContestEntry) + "/.json?auth=" + str(self.firebaseToken), data=json.dumps(newKAContestEntries[contestWithNewEntries][newContestEntry]), headers={"content-type": "application/json"})
                if addEntryReq.status_code == 200:
                    requests.put(self.firebaseApp + "/contests/" + str(contestWithNewEntries) + "/entryKeys/" + str(newContestEntry) + "/.json?auth=" + str(self.firebaseToken), data="true")
                else:
                    self.output("PUT Request to Firebase failed while attempting to push new contest entries. Status Code: " + str(addEntryReq.status_code), "FATAL")

        # Phase 4: Remove old data
        # ...
        # NOTE: https://github.com/sparkstudios/CJSKA-Sync-Bot/issues/1
        for contestWithDelEntries in delKAContestEntries:
            for delContestEntry in delKAContestEntries[contestWithDelEntries]:
                delEntryReq = requests.put(self.firebaseApp + "/contests/" + str(contestWithDelEntries) + "/entries/" + str(delContestEntry) + "/archived/.json?auth=" + str(self.firebaseToken), data="true")

        self.output("Sync loop finished")
        endTime = time.time()
        self.output("Sync loop took approximately " + str(round(endTime - startTime, 2)) + " seconds")

    def runBot(self):
        self.output("SyncBot starting infinite loop.")
        while True:
            self.sync()

            self.output("Returning to idle state.")
            time.sleep(self.wait)
        self.output("Infinite loop terminated.")
