import os

def check_login():
    print(os.environ)
    if 'HTTP_COOKIE' in os.environ:
        cookies = os.environ['HTTP_COOKIE'].split(';')
        for cookie in cookies:
            return cookie.strip()
    else:
        return 'hi'
