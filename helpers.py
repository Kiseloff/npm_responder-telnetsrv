import re
import datetime


def remove_backspaces(s):
    while True:
        # if you find a character followed by a backspace, remove both
        t = re.sub('.\b', '', s, count=1)
        if len(s) == len(t):
            # now remove any backspaces from beginning of string
            return re.sub('\b+', '', t)
        s = t


def log(file, msg, logtime=True, output=True):
    """
    Log MSG to file

    :param str file: path to log file
    :param str msg: message to log
    :param bool logtime: add time to MSG
    :param output: send MSG to console
    """
    if logtime:
        msg = ' --- '.join([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg.lstrip()])
    if output:
        print(msg)

    with open(file, 'a') as f:
        f.write(msg + '\n')
