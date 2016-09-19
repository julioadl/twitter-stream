import twitterStream as t
import os
import httplib
import time
import threading

#Function that calls the twitterStream
def beginStream():
    #Activate the streaming services
    try:
        stream = t.twitterStream()
        stream.fetchsamples()

    except httplib.IncompleteRead:
        pass

    #Recursively call the streaming
    threading.Timer(1.0, beginStream).start()

keywords = []
beginStream()
