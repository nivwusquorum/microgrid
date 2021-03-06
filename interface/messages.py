# This should be identical to messages.h in comm_board code.
class ToUlink(object):
    PING = 0
    GET_SETTINGS = 1
    SET_TIME = 2
    CRON_STATS = 3
    RESET_PIC = 4
    GET_MEMORY = 5
    SET_UID_NODE_TYPE = 6
    SET_BALANCE = 7
    READ_EEPROM = 8
    DATA_LOGGER = 9
    PONG = 10
    GET_CONNECTED_NODES = 11
    TEST_LEDS = 12
    PRINT_LOCAL_TIME = 13
    DEMAND_REPONSE = 14
    OVERRIDE_DEMAND_REPONSE = 15
    PRINT_DATA_LOGS = 16
    SET_STATE_OF_CHARGE = 17
    SET_BATTERY_CAPACITY = 18
    SET_THRESHOLDS = 19
    SET_BALANCE_UPDATE = 20
    FACTORY_RESET = 21


class ToComputer(object):
    DEBUG = 0
    GET_SETTINGS_REPLY = 1
    DATA_LOGGER_REPLY = 2
