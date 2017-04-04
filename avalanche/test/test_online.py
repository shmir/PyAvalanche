"""
Avalanche package tests that require actual Avalanche chassis/appliance and active ports.

Test setup:
Two Avalanche ports connected back to back.

@author yoram@ignissoft.com
"""

from os import path

from avalanche.test.test_base import AvlTestBase


class AvlTestOnline(AvlTestBase):

    ports = []

    def testOnline(self):
        """ Load configuration on ports and verify that ports are online. """
        self.logger.info(AvlTestOnline.testOnline.__doc__.strip())

        self.avl.load_config(path.join(path.dirname(__file__), 'configs/test_config.tcc'))

        self.avl.connect(self.config.get('AVL', 'chassis'))

        self._reserve_ports()

        for port in self.ports:
            assert(port.is_online())

        for port in self.ports:
            port.release()

        self.stc.project.get_object_by_name('Port 1').reserve(wait_for_up=False)
        self.stc.project.get_object_by_name('Port 2').reserve(wait_for_up=False)

        pass

    def _reserve_ports(self):
        pass
