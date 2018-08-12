"""
Avalanche package tests that require actual Avalanche chassis/appliance and active ports.

Test setup:
Two Avalanche ports connected back to back.

@author yoram@ignissoft.com
"""

from os import path
import json
import time

from avalanche.avl_object import AvlObject
from avalanche.avl_project import AvlAssociation, AvlInterface
from avalanche.avl_statistics_view import AvlClientStats
from avalanche.test.test_base import TestAvlBase


class TestAvlOnline(TestAvlBase):

    ports = []

    def test_inventory(self):
        """ Get chassis inventory. """
        self.logger.info(TestAvlOnline.test_inventory.__doc__.strip())

        ip, module, port = self.config.get('Client', 'association_1').split('/')
        chassis = self.avl.hw.get_chassis(ip)
        chassis.get_inventory()
        print chassis.modules
        print chassis.modules[int(module)].ports

    def test_reserve_ports(self):
        """ Load configuration on ports and verify that ports are online. """
        self.logger.info(TestAvlOnline.test_reserve_ports.__doc__.strip())

        self.avl.load_config(path.join(path.dirname(__file__), 'configs/test_config.spf'))
        self._reserve_ports(self.config.get('Client', 'association_1'),
                            self.config.get('Server', 'association_1'))
        self.avl.project.tests['Test'].client.associations[1].interface.set_port(self.config.get('Client', 'association_1'))
        self.avl.project.tests['Test'].server.associations[1].interface.set_port(self.config.get('Server', 'association_1'))

    def test_run_wait(self):
        """ Load configuration on ports, run test and wait for test to complete. """
        self.logger.info(TestAvlOnline.test_run_wait.__doc__.strip())

        self.test_reserve_ports()

        client_stats = AvlClientStats(self.avl.project, 'http')
        client_stats.read_stats()
        print(json.dumps(client_stats.statistics, indent=2))
        self.avl.project.tests['Test'].start(trial=True, blocking=True)
        client_stats.read_stats()
        print(json.dumps(client_stats.statistics, indent=2))

    def test_new_config(self):
        """ Create new configuration. """
        self.logger.info(TestAvlOnline.test_new_config.__doc__.strip())

        # Create project and test.
        self.avl.new_config()
        test = self.avl.project.new_test()

        clinet_interface = AvlInterface(parent=test.topology, side='client')
        server_interface = AvlInterface(parent=test.topology, side='server')

        # Create associations (first create associations with interfaces only then config the other relations).
        for _ in range(0, 3):
            AvlAssociation(parent=test.client, association_type='globalassociations',
                           associated_interface=clinet_interface.ref)
        AvlAssociation(parent=test.server, associated_interface=server_interface.ref)

        # Create loads.
        for height in [2, 20]:
            load = AvlObject(objType='load', parent=self.avl.project, name='SU_{}'.format(height * 5))
            load.set_attributes(loadSpecification='Sessions')
            steps = load.get_child('steps').get_children('step')
            steps[1].delete()
            del steps[1]
            for step in steps:
                step.set_attributes(height=0)
            steps[1].set_attributes(height=height, num=5)
            steps[2].set_attributes(steadyTime=20)

        # Create action lists.
        for rate in ['1K', '10K', '100K']:
            action = AvlObject(objType='actionlist', parent=self.avl.project, name='HTTP_' + rate)
            action.set_attributes(filecontents='1 get http://192.168.1.1/' + rate)

        # Create client subnects.
        for network in ['1.1.1', '2.2.2', '3.3.3']:
            subnet = AvlObject(objType='clientsubnet', parent=self.avl.project, name='Net_' + network)
            attributes = {'network': '{}.0'.format(network),
                          'ipaddressranges.ipaddressrange': '{}.1-{}.100'.format(network, network)}
            subnet.set_attributes(**attributes)

        # Set load.
        test.client.set_attributes(loadProfile=self.avl.project.get_objects_by_type('load')[0])

        # Create server transactions to match action lists.
        for rate in ['1K', '10K', '100K']:
            transaction = AvlObject(objType='transaction', parent=self.avl.project, name=rate)
            transaction.set_attributes(bodyBytes=int(rate[:-1]) * 1024)

        # Create server subnet.
        subnet = AvlObject(objType='serversubnet', parent=self.avl.project, name='Net_Server')

        # Tie all under association.
        for i, association in enumerate(test.client.get_objects_by_type('association')):
            association.set_attributes(userActions=self.avl.project.get_objects_by_type('actionlist')[i].name,
                                       clientSubnet=self.avl.project.get_objects_by_type('clientsubnet')[i].name)
        association = test.server.get_object_by_type('association')
        association.set_attributes(serverSubnet=self.avl.project.get_object_by_type('serversubnet'),
                                   ipAddressRange='192.168.1.1-192.168.1.3')

        # Save configuration.
        self.avl.save_config(path.join(path.dirname(__file__), 'configs/new_test_config.spf'))

    def test_build_and_run(self):
        """ Build configuration, attach ports, run test and wait for test to complete. """
        self.logger.info(TestAvlOnline.test_build_and_run.__doc__.strip())

        # Create new configuration.
        self.test_new_config()
        self.test_reserve_ports()

        # Reserve ports
        # self._reserve_ports('10.241.17.207/1/1', '10.241.17.207/1/2')

        # Assign ports to associations.
        # self.avl.project.tests['Test'].client.associations[1].interface.set_port('10.241.17.207/1/1')
        # self.avl.project.tests['Test'].server.associations[1].interface.set_port('10.241.17.207/1/2')

        # Save configuration.
        # self.avl.save_config(path.join(path.dirname(__file__), 'configs/new_test_config.spf'))

        # Subscribe to statistics.
        http_stats = AvlClientStats(self.avl.project, 'http')
        simusers_stats = AvlClientStats(self.avl.project, 'simusers')
        tcp_stats = AvlClientStats(self.avl.project, 'tcp')

        # Start test.
        self.avl.project.tests['Test'].start(trial=True, blocking=True)
        time.sleep(4)

        # Get statistics.
        http_stats.read_stats()
        print(json.dumps(http_stats.statistics, indent=2))
        simusers_stats.read_stats()
        print(json.dumps(simusers_stats.statistics, indent=2))
        tcp_stats.read_stats()
        print(json.dumps(tcp_stats.statistics, indent=2))

    def test_run_stop(self):
        """ Load configuration on ports, run test and wait for test to complete. """
        self.logger.info(TestAvlOnline.test_run_stop.__doc__.strip())

        self.test_reserve_ports()
        self.avl.project.tests['Test'].start(trial=True)
        self.avl.project.tests['Test'].stop()

    def _reserve_ports(self, *locations):
        chassis_list = []
        for location in locations:
            ip, module, port = location.split('/')
            chassis = self.avl.hw.get_chassis(ip)
            if chassis not in chassis_list:
                chassis.get_inventory()
                chassis_list.append(chassis)
            chassis.modules[int(module)].ports[int(port)].reserve()
