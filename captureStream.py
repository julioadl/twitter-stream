import twitterStream as t
import sys

keywords = ["RenunciaYa", "#RenunciaYa", "@EPN", "EPN"]
t = t.twitterStream()
t.fetchsamples(keywords)
