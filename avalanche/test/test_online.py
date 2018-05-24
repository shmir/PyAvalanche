"""
Avalanche package tests that require actual Avalanche chassis/appliance and active ports.

Test setup:
Two Avalanche ports connected back to back.

@author yoram@ignissoft.com
"""

from avalanche.test.test_base import AvlTestBase


class AvlTestOnline(AvlTestBase):

    ports = []

    def test_inventory(self):
        """ Load configuration on ports and verify that ports are online. """
        self.logger.info(AvlTestOnline.test_inventory.__doc__.strip())
        ip, module, port = self.config.get('AVL', 'port1').split('/')
        chassis = self.avl.hw.get_chassis(ip)
        chassis.get_inventory()
        print chassis.modules
        print chassis.modules[int(module)].ports

    def test_reserve_ports(self):
        """ Load configuration on ports and verify that ports are online. """
        self.logger.info(AvlTestOnline.test_inventory.__doc__.strip())
        ip, module, port = self.config.get('AVL', 'port1').split('/')
        chassis = self.avl.hw.get_chassis(ip)
        chassis.get_inventory()
        chassis.modules[int(module)].ports[int(port)].reserve()

    def _reserve_ports(self):
        self.avl.hw.get_port(self.config.get('AVL', 'port1')).reserve()
        self.avl.hw.get_port(self.config.get('AVL', 'port2')).reserve()
