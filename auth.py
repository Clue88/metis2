import os

def check_login():
    if 'HTTP_COOKIE' in os.environ:
        cookies = os.environ['HTTP_COOKIE'].split(';')
        return False
    else:
        return False
