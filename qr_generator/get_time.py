import datetime

def get_current_time():
    now = str(datetime.datetime.now()).split('.')
    return now[1]


print(get_current_time())