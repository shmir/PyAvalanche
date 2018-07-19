"""
Avalanche package tests that can run in offline mode.

@author yoram@ignissoft.com
"""

from os import path

from avalanche.avl_object import AvlObject
from avalanche.avl_project import AvlAssociation, AvlInterface
from avalanche.test.test_base import AvlTestBase


class AvlTestOffline(AvlTestBase):

    def testLoadConfig(self):
        """ Load existing configuration. """
        self.logger.info(AvlTestOffline.testLoadConfig.__doc__.strip())

        self.avl.load_config(path.join(path.dirname(__file__), 'configs/ExportedProjects.spf'))
        file_name, file_ext = path.splitext(path.join(path.dirname(__file__), 'configs/ExportedProjects.spf'))
        self.avl.save_config(file_name + '_save' + file_ext)

    def testNewConfig(self):
        """ Create new configuration. """
        self.logger.info(AvlTestOffline.testNewConfig.__doc__.strip())

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

    def testAnalyzeConfig(self):
        """ Analyze existing configuration. """
        self.logger.info(AvlTestOffline.testAnalyzeConfig.__doc__.strip())

        self.avl.load_config(path.join(path.dirname(__file__), 'configs/test_config.spf'))
        assert(len(self.avl.project.tests) == 3)
