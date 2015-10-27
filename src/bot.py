import sys
import requests
import json
from firebase_token_generator import create_token

def getFirebaseToken(secret, uid):
    return create_token(secret, {"uid": uid})

def main(firebaseSecret, firebaseUID):
    if firebaseSecret != "MY_FIREBASE_SECRET" and firebaseUID != "MY_FIREBASE_UID":
        fbToken = getFirebaseToken(firebaseSecret, firebaseUID)
    else:
        print("Uh-oh! It looks like you forgot to include a valid Firebase Secret and/or a valid Firebase UID.")
        return

print("Command Line arguments: " + str(sys.argv))
try:
    main(str(sys.argv[1]), str(sys.argv[2]))
except IndexError:
    print("Sorry, we couldn't find the correct command line argument. Exiting!")
