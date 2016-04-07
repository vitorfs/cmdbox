import urllib
import hashlib


def get_gravatar_url(email, size=40):
    gravatar_url = 'http://www.gravatar.com/avatar/' + hashlib.md5(email.lower()).hexdigest() + '?'
    gravatar_url += urllib.urlencode({'d': 'mm', 's': str(size)})
    return gravatar_url
