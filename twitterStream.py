import json
import datetime
import oauth2 as oauth
import urllib2 as urllib


'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''

class twitterStream:

  def twitterreq(self, url, method, parameters):

    access_token_key = "589408945-MUbg17aThZY2jxVgTDRZrTI4tMizGTeKqUDC54ZM"
    access_token_secret = "aIawDKoNExONU980WE1BTZi4is56T40snRX7mrJR77Y"

    consumer_key = "hqVR1b1W4BW8yWi1pbJUp0nrm"
    consumer_secret = "7GAbZeVv5rihyCERRB9pWNaRZHrXMPCe3NtNCKiupGzhxvZkuh"

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

    tweets = {'tweets': []}
    date = datetime.datetime.now().isoformat()
    name_file = '/tweets-' + str(date) + '.txt'
    with open(name_file, 'w') as textFile:
        for line in response:
            tweet = line.strip()
            textFile.write(tweet + '\n')