import urllib
import hashlib
import hmac
import re

def percent_encode(string):
    """A version of urllibs' quote which correctly quotes '~'"""
    return urllib.quote(string.encode('utf-8'), '~')

def to_query(obj, ns=None):
    """Create a query string from a list or dictionary"""
    if isinstance(obj, dict):
        pairs = sum((to_query(v, u"{0}[{1}]".format(ns, k) if ns else k)
                     for k, v in obj.items()), [])
        if ns:
            return pairs
        return u"&".join(u"{0}={1}".format(*p) for p in sorted(pairs))
    elif isinstance(obj, (list, tuple)):
        return sum((to_query(v, u"{0}[]".format(ns)) for v in obj), [])
    else:
        return [(percent_encode(unicode(ns)), percent_encode(unicode(obj)))]

def generate_signature(data, secret):
    """
    signature takes a dict / tuple /string
    and your application's secret, returning a HMAC-SHA256
    digest of the data.
    """
    return hmac.new(secret, to_query(data), hashlib.sha256).hexdigest()

def signature_valid(data, secret):
    params = data.copy()
    sig = params.pop("signature")
    valid_sig = generate_signature(params, secret)
    return sig == valid_sig

def camelize(to_uncamel):
    result = []
    for word in re.split("_", to_uncamel):
        result.append(word[0].upper() + word[1:])
    return "".join(result)

def singularize(to_sing):
    return re.sub("s$", "", to_sing)
