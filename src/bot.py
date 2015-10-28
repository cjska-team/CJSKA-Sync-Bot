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
        self.firebaseApp = "https://kacjs-dev.firebaseio.com"

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

        kaContestsAdded = [] # Contests to add to Firebase
        fbContestsDelete = [] # Contests to delete from Firebase

        kaContestEntriesAdded = {} # Contests Entries to add to Firebase
        kaContestEntriesDeleted = {} # Contest Entries to delete from Firebase

        # Phase 1: Check for new data
        self.output("Beginning Sync Phase 1 (Checking for new content)", "DiffCheck")
        for kaContest in kaContests:
            if kaContest in fbContests:
                # Check for new contest entries
                # ...

                kaContestEntriesAdded[str(kaContest)] = []

                self.output("Fetching contest entries from Khan Academy (for contest with ID " + kaContest + ")", "DiffCheck")
                kaContestEntries = kaApiWrapper.getContestEntries(kaContest)

                self.output("Fetching contest entries stored in Firebase (for contest with ID " + kaContest + ")", "DiffCheck")
                fbContestEntries = self.getStoredContestEntries(kaContest)

                for kaContestEntry in kaContestEntries:
                    if kaContestEntry in fbContestEntries:
                        pass
                    else:
                        self.output("Untracked contest entry found. Contest ID: " + str(kaContest) + " Entry ID: " + str(kaContestEntry), "DiffCheck")
                        kaContestEntriesAdded[str(kaContest)].append(str(kaContestEntry))
            else:
                self.output("Untracked contest found. ID: " + str(kaContest), "DiffCheck")
                kaContestsAdded.append(str(kaContest))

        # Phase 2: Check for deleted data
        self.output("Beginning Sync Phase 2 (Checking for deleted content)", "DiffCheck")
        for fbContest in fbContests:
            if fbContest in kaContests:
                # Check for deleted contest entries
                # ...

                kaContestEntriesDeleted[str(fbContest)] = []

                self.output("Fetching contest entries from Khan Academy (for contest with ID " + fbContest + ")", "DiffCheck")
                kaContestEntries = kaApiWrapper.getContestEntries(fbContest)

                self.output("Fetching contest entries stored in Firebase (for contest with ID " + fbContest + ")", "DiffCheck")
                fbContestEntries = self.getStoredContestEntries(fbContest)

                for fbContestEntry in fbContestEntries:
                    if fbContestEntry in kaContestEntries:
                        pass
                    else:
                        self.output("Found a contest entry that no longer exists. Contest ID: " + str(fbContest) + " Entry ID: " + str(fbContestEntry), "DiffCheck")
                        kaContestEntriesDeleted[str(fbContest)].append(str(fbContestEntry))
            else:
                self.output("Found a contest that no longer exists. ID: " + str(fbContest), "DiffCheck")
                fbContestsDelete.append(str(fbContest))


        self.output("Untracked contests: " + str(kaContestsAdded), "DiffDebug")
        self.output("Contests with untracked entries: " + str(kaContestEntriesAdded), "DiffDebug")

        # Phase 3: Write new data
        # TODO: Push the actual scratchpad data to Firebase!
        # P3A: Write new contests
        for newContest in range(0, len(kaContestsAdded)):
            # 2 PUT requests to:
            # /contestKeys/<contestId>: true
            # /contests/<contestId>: <contestDataJSON>
            requests.put(self.firebaseApp + "/contestKeys/" + str(kaContestsAdded[newContest]) + "/.json?auth=" + str(self.firebaseToken), data="true")

        # P3B: Write new contest entries
        for contestWithNewEntries in kaContestEntriesAdded:
            for newContestEntry in range(0, len(kaContestEntriesAdded[contestWithNewEntries])):
                requests.put(self.firebaseApp + "/contests/" + str(contestWithNewEntries) + "/entryKeys/" + str(kaContestEntriesAdded[contestWithNewEntries][newContestEntry]) + "/.json?auth=" + str(self.firebaseToken), data="true")

        # Phase 4: Remove old data
        # ...
        # NOTE: https://github.com/sparkstudios/CJSKA-Sync-Bot/issues/1

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
