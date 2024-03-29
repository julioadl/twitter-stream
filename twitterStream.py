import json
import pymongo
import datetime
import oauth2 as oauth
import urllib.request as urllib

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''

class twitterStream:

  def twitterreq(self, url, method, parameters):

    access_token_key = ""
    access_token_secret = ""

    consumer_key = ""
    consumer_secret = ""

    _debug = 0

    oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
    oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

    signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

    http_method = "GET"

    http_handler  = urllib.HTTPHandler(debuglevel=_debug)
    https_handler = urllib.HTTPSHandler(debuglevel=_debug)

    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                token=oauth_token,
                                                http_method=http_method,
                                                http_url=url,
                                                parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
      encoded_post_data = req.to_postdata()
    else:
      encoded_post_data = None
      url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response

  def fetchsamples(self, keywordList):


    keywordList = keywordList

    toTrack = ",".join(keywordList)

    url = "https://stream.twitter.com/1.1/statuses/filter.json?track=" + toTrack
    parameters = []
    response = self.twitterreq(url, "GET", parameters)

    conn = pymongo.MongoClient('mongodb://localhost:27017')
    db = conn.sandbox

    for line in response:
        tweet = line.strip()
        try:
            tweet = json.loads(tweet)
            db.tweets.insert(tweet)
        except:
            pass
