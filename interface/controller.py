import struct
import time

from kivy.clock import Clock

from data_logger import DataLogger
from messages import ToUlink, ToComputer
from utils import MessageBuilder

class Ctrl(object):
    def __init__(self, root):
        self.ui_root = root
        self.data_logger = DataLogger(self.ui_root)

        Clock.schedule_interval(self.update_indicators, 0.2)
        Clock.schedule_interval(self.update_settings, 1.0)
        Clock.schedule_interval(self.ui_root.update_serial_choices, 1.0)

    def send(self, msg):
        if self.ui_root.serial:
            self.ui_root.serial.send(msg)

    def clear_logs(self):
        self.ui_root.debug_panel.logs.adapter.data = []

    def send_ping(self):
        mb = MessageBuilder(ToUlink.PING)
        self.send(mb.to_bytes())

    def test_leds(self):
        mb = MessageBuilder(ToUlink.TEST_LEDS)
        self.send(mb.to_bytes())

    def print_local_time(self):
        mb = MessageBuilder(ToUlink.PRINT_LOCAL_TIME)
        self.send(mb.to_bytes())

    def override_demand_response_state(self):
        mb = MessageBuilder(ToUlink.OVERRIDE_DEMAND_REPONSE)
        state_to_command = {
            'none':   [0, 0],
            'green':  [1, 0],
            'yellow': [1, 1],
            'red':    [1, 2],
            'off':    [1, 3],
            'on':     [1, 4],
        }
        target_state = self.ui_root.debug_panel.dr_state.text
        if target_state not in state_to_command.keys():
            print ('%s not acceptable. Must be one of %s..' % (target_state, state_to_command.keys()))
            return
        for b in state_to_command[target_state]:
            mb.add_byte(b)
        self.send(mb.to_bytes())

    def print_data_logs(self):
        mb = MessageBuilder(ToUlink.PRINT_DATA_LOGS)
        self.send(mb.to_bytes())

    def cron_stats(self):
        mb = MessageBuilder(ToUlink.CRON_STATS)
        self.send(mb.to_bytes())


    def update_settings(self, *largs):
        mb = MessageBuilder(ToUlink.GET_SETTINGS)
        self.send(mb.to_bytes())

    def get_memory(self):
        mb = MessageBuilder(ToUlink.GET_MEMORY)
        self.send(mb.to_bytes())

    def sync_time(self):
        ts = int(time.time())
        mb = MessageBuilder(ToUlink.SET_TIME)
        mb.add_uint32(ts)
        self.send(mb.to_bytes())

    def set_uid_node_type(self):
        mb = MessageBuilder(ToUlink.SET_UID_NODE_TYPE)
        try:
            uid = int(self.ui_root.settings.box_uid.text)
            assert 0<= uid and uid <= 255
            node_type = self.ui_root.settings.box_node_type.text
            node_type = node_type.upper()
            assert len(node_type) == 1 and node_type in ['A', 'B']
            node_type = ord(node_type)
            mb.add_byte(uid)
            mb.add_byte(node_type)
            self.send(mb.to_bytes())
        except Exception as e:
            print (e)
            print ('WARNING: invalid uid or node type value.')

    def set_balance(self):
        try:
            mb = MessageBuilder(ToUlink.SET_BALANCE)
            balance = int(self.ui_root.settings.box_balance.text)
            mb.add_uint32(balance)
            self.send(mb.to_bytes())
        except Exception as e:
            print (e)
            print ('WARNING: invalid balance value.')

    def set_state_of_charge(self):
        try:
            mb = MessageBuilder(ToUlink.SET_STATE_OF_CHARGE)
            state = float(self.ui_root.settings.state_of_charge.text)
            uncertainty = float(self.ui_root.settings.uncertainty_of_charge.text)
            mb.add_float(state)
            mb.add_float(uncertainty)
            self.send(mb.to_bytes())
        except Exception as e:
            print (e)
            print ('WARNING: wrong state of charge value.')

    def set_battery_capacity(self):
        try:
            mb = MessageBuilder(ToUlink.SET_BATTERY_CAPACITY)
            battery_capacity = float(self.ui_root.settings.battery_capacity.text)
            mb.add_float(battery_capacity)
            self.send(mb.to_bytes())
        except Exception as e:
            print (e)
            print ('WARNING: wrong battery capacity value.')

    def set_thresholds(self):
        try:
            mb = MessageBuilder(ToUlink.SET_THRESHOLDS)

            off_threshold = float(self.ui_root.settings.off_threshold.text)
            red_threshold = float(self.ui_root.settings.red_threshold.text)
            yellow_threshold = float(self.ui_root.settings.yellow_threshold.text)

            mb.add_float(off_threshold)
            mb.add_float(red_threshold)
            mb.add_float(yellow_threshold)

            self.send(mb.to_bytes())
        except Exception as e:
            print (e)
            print ('WARNING: wrong state of charge value.')

    def set_balance_update(self):
        try:
            mb = MessageBuilder(ToUlink.SET_BALANCE_UPDATE)

            balance_update_hours   = int(self.ui_root.settings.balance_update_hours.text)
            balance_update_minutes = int(self.ui_root.settings.balance_update_minutes.text)
            balance_update_ammount = int(self.ui_root.settings.balance_update_ammount.text)

            assert(balance_update_hours in range(24))
            assert(balance_update_minutes in range(60))
            assert(balance_update_ammount > 0)

            mb.add_int(balance_update_hours)
            mb.add_int(balance_update_minutes)
            mb.add_uint32(balance_update_ammount)

            self.send(mb.to_bytes())
        except Exception as e:
            print (e)
            print ('WARNING: wrong values for balance update')

    def factory_reset(self):
        mb = MessageBuilder(ToUlink.FACTORY_RESET)
        self.send(mb.to_bytes())

    def reset_pic(self):
        mb = MessageBuilder(ToUlink.RESET_PIC)
        self.send(mb.to_bytes())

    def get_connected_nodes(self):
        mb = MessageBuilder(ToUlink.GET_CONNECTED_NODES)
        self.send(mb.to_bytes())

    def read_eeprom(self, mem_type):
        mem_types = [ 'float', 'uint32', 'byte']
        assert mem_type in mem_types
        mem_type_idx = mem_types.index(mem_type)
        addr = None
        try:
            addr = int(self.ui_root.debug_panel.eeprom_addr.text)
        except Exception as e:
            print (e)
            print ('WARNING: invalid eeprom_addr')

        mb = MessageBuilder(ToUlink.READ_EEPROM)
        mb.add_byte(mem_type_idx)
        mb.add_uint32(addr)
        self.send(mb.to_bytes())

    def update_indicators(self, *largs):
        if self.ui_root.serial:
            inbound, outbound = self.ui_root.serial.pop_recent_traffic()
            self.ui_root.indicators.update(inbound, outbound)

get = None
