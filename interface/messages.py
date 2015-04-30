# This should be identical to messages.h in comm_board code.
class ToUlink(object):
    PING = 0
    GET_TIME = 1
    SET_TIME = 2
    CRON_STATS = 3
    RESET_PIC = 4
    GET_MEMORY = 5

class ToComputer(object):
    DEBUG = 0
    GET_TIME_REPLY = 1
