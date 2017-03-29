"""
This module implements classes and utility functions to manage Avalanche application.

:author: yoram@ignissoft.com
"""

from os import path
import time
from random import randint


from trafficgenerator.trafficgenerator import TrafficGenerator

from avalanche.avl_object import AvlObject
from avalanche.avl_hw import AvlPhyChassis

TYPE_2_OBJECT = {}


class AvlApp(TrafficGenerator):
    """ TestCenter driver. Equivalent to TestCenter Application. """

    lab_server = None

    system = None
    project = None

    def __init__(self, logger, api_wrapper):
        """ Set all kinds of application level objects - logger, api, etc.

        :param logger: python logger (e.g. logging.getLogger('log'))
        :param api_wrapper: api wrapper object inheriting and implementing StcApi base class.
        """

        super(self.__class__, self).__init__()
        self.logger = logger
        self.api = api_wrapper

        AvlObject.logger = self.logger
        AvlObject.api = self.api
        AvlObject.str_2_class = TYPE_2_OBJECT

        self.system = AvlObject(objType='system', objRef='system1', parent=None)
        self.api.avl_command('login {}'.format(randint(0, 999)))

    def connect(self, chassis):
        """ Create object and (optionally) connect to lab server.

        :param lab_server: optional lab server address.
        """

        self.hw = self.system.get_child('PhysicalChassisManager')
        chassis_ref = self.api.avl_command("connect {}".format(chassis))
        chassis = AvlPhyChassis(objType='PhysicalChassis', parent=self.hw, objRef=chassis_ref)
#         chassis.get_inventory()

    def disconnect(self):
        """ Disconnect from chassis and shutdown. """

        for chassis in self.hw.get_objects_by_type('PhysicalChassis'):
            self.api.avl_command("disconnect {}".format(chassis.get_attribute('IpAddress')))
        self.api.avl_command("logout shutdown")

    def load_config(self, config_file_name):
        """ Load configuration file from tcc or xml.

        Configuration file type is extracted from the file suffix - xml or tcc.

        :param config_file_name: full path to the configuration file.
        """

        ext = path.splitext(config_file_name)[-1].lower()
        if ext == '.tcc':
            self.api.perform('LoadFromDatabase', DatabaseConnectionString=path.normpath(config_file_name))
        elif ext == '.xml':
            self.api.perform('LoadFromXml', FileName=path.normpath(config_file_name))
        else:
            raise ValueError('Configuration file type {} not supported.'.format(ext))

    def reset_config(self):
        self.api.perform('ResetConfig', config='system1')

    def save_config(self, config_file_name):
        """ Save configuration file as tcc or xml.

        Configuration file type is extracted from the file suffix - xml or tcc.
        :param config_file_name: full path to the configuration file.
        """

        ext = path.splitext(config_file_name)[-1].lower()
        if ext == '.tcc':
            self.api.perform('SaveToTcc', FileName=path.normpath(config_file_name))
        elif ext == '.xml':
            self.api.perform('SaveAsXml', FileName=path.normpath(config_file_name))
        else:
            raise ValueError('Configuration file type {0} not supported.'.format(ext))

    def clear_results(self):
        self.project.clear_results()

    #
    # Online commands.
    # All commands assume that all ports are reserved and port objects exist under project.
    #

    #
    # Devices commands.
    #

    def start_devices(self):
        """ Start all devices.

        It is the test responsibility to wait for devices to reach required state.
        """
        self._command_devices('DeviceStart')

    def stop_devices(self):
        self._command_devices('DeviceStop')

    def _command_devices(self, command):
        self.project.command_devices(command, 4)
        self.project.test_command_rc('Status')
        time.sleep(4)

    #
    # Traffic commands.
    #

    def start_traffic(self, blocking=False):
        self.project.start_ports(blocking)

    def stop_traffic(self):
        self.project.stop_ports()

    def wait_traffic(self):
        self.project.wait_traffic()
