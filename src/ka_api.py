import requests
import json

class KA_API:
    dummy = "KA_API"
    def __init__(self):
        self.urls = {
            "spotlight": "https://www.khanacademy.org/api/internal/scratchpads/top?casing=camel&topic_id=xffde7c31&sort=4&limit=40000&page=0&lang=en&_=1436581332879",
            "spinoffs" : "https://www.khanacademy.org/api/internal/scratchpads/{SCRATCHPAD}/top-forks?casing=camel&sort=2&limit=300000&page=0&lang=en",
            "scratchpadInfo": "https://www.khanacademy.org/api/labs/scratchpads/{SCRATCHPAD}"
        }
    def getContestEntries(self, contestId):
        newEntries = {}
        apiReq = requests.get(str(self.urls["spinoffs"]).replace("{SCRATCHPAD}", contestId))

        return apiReq.json()["scratchpads"]

    def numberOfEntriesInContest(self, contestId):
        return len(self.getContestEntries(contestId))

    def getContests(self):
        contests = {}
        apiReq = requests.get(str(self.urls["spotlight"]))
        responseJSON = apiReq.json()["scratchpads"]

        for i in range(0, len(responseJSON)):
            # Used for testing, please ignore.
            # print("===")
            # for prop in responseJSON[i]:
            #     print(prop)
            currScratchpad = responseJSON[i]

            if str(currScratchpad["authorNickname"]).rfind("pamela") != -1:
                # We've found a program that was most likely created by Pamela...
                if str(currScratchpad["translatedTitle"]).rfind("Contest") != -1 or str(currScratchpad["translatedTitle"]).rfind("contest") != -1:
                    # We probably just found a contest program created by Pamela...
                    scratchpadId = str(currScratchpad["url"]).split("/")[5]
                    scratchpadName = currScratchpad["translatedTitle"]
                    scratchpadImg = currScratchpad["thumb"]
                    scratchpadRubrics = {}
                    scratchpadDesc = ""

                    try:
                        scratchpadDesc = currScratchpad["description"]
                    except KeyError:
                        pass

                    tmpContest = {
                        "id": scratchpadId,
                        "name": scratchpadName,
                        "desc": scratchpadDesc,
                        "img": scratchpadImg,
                        "rubrics": scratchpadRubrics
                    }

                    # print(tmpContest)

                    contests[scratchpadId] = tmpContest

        return contests

    def test(self):
        testsToRun = [
            self.getContests
        ]

        i = 0

        while i < len(testsToRun):
            print(testsToRun[i]())
            i = i + 1
