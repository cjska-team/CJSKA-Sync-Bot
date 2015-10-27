#!/bin/bash
# Run the CJSKA Sync Bot

FIREBASE_SECRET=MY_FIREBASE_SECRET # TODO: Replace "MY_FIREBASE_SECRET" with Firebase Secret before running
FIREBASE_USERID=MY_FIREBASE_UID # TODO: Replace "MY_FIREBASE_UID" with the correct Firebase UID before running

python3 src/bot.py $FIREBASE_SECRET $FIREBASE_USERID
