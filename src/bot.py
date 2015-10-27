import sys
import requests
import json

def main(firebaseSecret):
    if firebaseSecret == "MY_FIREBASE_SECRET":
        print("Uh-oh! It looks like you forgot to include a valid Firebase Secret.")
        return
    else:
        print("TODO (Gigabyte Giant): Write this!")

print("Command Line arguments: " + str(sys.argv))
try:
    main(str(sys.argv[1]))
except IndexError:
    print("Sorry, we couldn't find the correct command line argument. Exiting!")
