"""
This module implements classes and utility functions to manage Avalanche application.

:author: yoram@ignissoft.com
"""

from os import path
from random import randint
import shutil

from trafficgenerator.trafficgenerator import TrafficGenerator

from avalanche.avl_object import AvlObject
from avalanche.avl_project import AvlProject, AvlTest, AvlServer
from avalanche.avl_hw import AvlPhyChassis

TYPE_2_OBJECT = {'tests': AvlTest,
                 'server': AvlServer}


class AvlApp(TrafficGenerator):
    """ TestCenter driver. Equivalent to TestCenter Application. """

    lab_server = None

    system = None
    project = None
    hw = None

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
        self.system.hw = None
        self.api.avl_command('login {}'.format(randint(0, 999)))

    def connect(self, chassis):
        """ Create object and (optionally) connect to lab server.

        :param lab_server: optional lab server address.
        """

        self.system.hw = self.system.get_child('PhysicalChassisManager')
        chassis_ref = self.api.avl_command("connect {}".format(chassis))
        chassis = AvlPhyChassis(objType='PhysicalChassis', parent=self.system.hw, objRef=chassis_ref)
        chassis.get_inventory()

    def disconnect(self):
        """ Disconnect from chassis and shutdown. """

        if self.system.hw:
            for chassis in self.hw.get_objects_by_type('PhysicalChassis'):
                self.api.avl_command("disconnect {}".format(chassis.get_attribute('IpAddress')))
        self.api.avl_command("logout shutdown")

    def load_config(self, config_file_name):
        """ Load configuration file from tcc or xml.

        :param config_file_name: full path to the configuration file.
        """

        project_ref = self.api.perform('import ' + self.system.obj_ref(), File=path.normpath(config_file_name))
        self.project = AvlProject(parent=self.system, objRef=project_ref)

    def save_config(self, config_file_name):
        """ Save configuration file as tcc or xml.

        :param config_file_name: full path to the configuration file.
        """

        self.api.perform('save ' + self.system.obj_ref())
        self.api.perform('export ' + self.system.obj_ref(), projectsTestsHandles=self.project.obj_ref())
        shutil.copy(self.system.get_attribute('latestExportedFile'), config_file_name)

    #
    # Online commands.
    # All commands assume that all ports are reserved and port objects exist under project.
    #

    #
    # Traffic commands.
    #

    def start_traffic(self, blocking=False):
        self.project.start_ports(blocking)

    def stop_traffic(self):
        self.project.stop_ports()

    def wait_traffic(self):
        self.project.wait_traffic()
