import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'B="\xb2\xffF\xc4j\xe5\x00\xadK\xd5\xe2\x87\xdf'

    MONGODB_SETTINGS = {'db' : 'bearit'}
