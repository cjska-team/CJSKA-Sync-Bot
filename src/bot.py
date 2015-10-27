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
        self.logFile = open(logFileLoc + "log_" + str(time.ctime()).replace(" ", "-") + ".txt", "w")

        self.output("SyncBot initialized")

    def output(self, msg, prefix="Sync  Bot"):
        currTime = str(time.ctime())
        print("(" + currTime + ") [" + prefix + "] - " + str(msg))
        self.logFile.write("(" + currTime + ") - " + msg + "\n")

    def getStoredContests(self):
        apiRequest = requests.get("https://contest-judging-sys.firebaseio.com/contestKeys.json?print=pretty")
        responseJSON = apiRequest.json()

        return responseJSON

    def getStoredContestEntries(self, contestId):
        apiRequest = requests.get("https://contest-judging-sys.firebaseio.com/contests/" + str(contestId) + "/entryKeys.json?print=pretty")
        responseJSON = apiRequest.json()

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
