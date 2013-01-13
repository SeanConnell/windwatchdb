#1/usr/bin/python

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('icarus/logs.%s' % (__name__))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler) 
logger.setLevel(logging.DEBUG)

TIME_FORMAT = '%Y%m%d%M'

cache = {}
#FIXME: Figure out how to clear this damned cache

def memoize(f):
    def memf(*x):
        if x not in cache:
            logger.debug("Memoization cache miss for %s" % str(x))
            cache[x] = f(*x)
            return cache[x]
        else:
            logger.debug("Memoization cache hit for %s" % str(x))
            return cache[x]
    return memf
