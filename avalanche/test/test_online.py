"""
Avalanche package tests that require actual Avalanche chassis/appliance and active ports.

Test setup:
Two Avalanche ports connected back to back.

@author yoram@ignissoft.com
"""

from avalanche.test.test_base import AvlTestBase


class AvlTestOnline(AvlTestBase):

    ports = []

    def testOnline(self):
        """ Load configuration on ports and verify that ports are online. """
        self.logger.info(AvlTestOnline.testOnline.__doc__.strip())

        pass

    def _reserve_ports(self):
        self.avl.system.hw.get_port(self.config.get('AVL', 'client/1')).reserve()
        self.avl.system.hw.get_port(self.config.get('AVL', 'client/1')).release()
        pass
