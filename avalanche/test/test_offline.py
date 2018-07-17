"""
Avalanche package tests that can run in offline mode.

@author yoram@ignissoft.com
"""

from os import path

from avalanche.avl_project import AvlActionList, AvlAssociation, AvlUserProfile, AvlInterface
from avalanche.test.test_base import AvlTestBase


class AvlTestOffline(AvlTestBase):

    def testLoadConfig(self):
        """ Load existing configuration. """
        self.logger.info(AvlTestOffline.testLoadConfig.__doc__.strip())

        self.avl.load_config(path.join(path.dirname(__file__), 'configs/test_config.spf'))
        file_name, file_ext = path.splitext(path.join(path.dirname(__file__), 'configs/test_config.spf'))
        self.avl.save_config(file_name + '-save' + file_ext)

    def testNewConfig(self):
        """ Create new configuration. """
        self.logger.info(AvlTestOffline.testNewConfig.__doc__.strip())

        self.avl.new_config()
        test = self.avl.project.new_test()

        clinet_interface = AvlInterface(parent=test.topology, side='client')
        server_interface = AvlInterface(parent=test.topology, side='server')

        client_association = AvlAssociation(parent=test.client, association_type='globalassociations')
        server_association = AvlAssociation(parent=test.server)
        action = AvlActionList(parent=self.avl.project)
        user_profile = AvlUserProfile(parent=self.avl.project)

        client_association.set_attributes(userActions=action.ref, userProfile=user_profile.ref,
                                          associatedInterface=clinet_interface.ref,
                                          clientsubnet=self.avl.project.get_child('clientsubnet').ref)
        server_association.set_attributes(ipAddressRange='192.168.1.1', associatedInterface=server_interface.ref)

        self.avl.save_config(path.join(path.dirname(__file__), 'configs/new_test_config.spf'))

    def testAnalyzeConfig(self):
        """ Analyze existing configuration. """
        self.logger.info(AvlTestOffline.testAnalyzeConfig.__doc__.strip())

        self.avl.load_config(path.join(path.dirname(__file__), 'configs/test_config.spf'))
        assert(len(self.avl.project.tests) == 3)
