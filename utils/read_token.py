def read_token():
    f = open('.token')
    token = f.read().split('\n')[0]
    f.close
    return token
