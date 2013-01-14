#!/usr/bin/python
def sanitize_string(string):
    return string.replace(' ','_').replace(',','').replace('\'','').replace('\"','').replace('\?','')
