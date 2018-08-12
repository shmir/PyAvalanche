"""
Base class for all Avalanche package tests.

@author yoram@ignissoft.com
"""

from os import path

from trafficgenerator.test.test_tgn import TestTgnBase

from avalanche.avl_app import init_avl


class TestAvlBase(TestTgnBase):

    TestTgnBase.config_file = path.join(path.dirname(__file__), 'Avalanche.ini')

    def setup(self):
        super(TestAvlBase, self).setup()
        self.avl = init_avl(self.logger, self.config.get('Tcl', 'install_dir'), self.config.get('AVL', 'install_dir'))
        self.avl.connect()

    def teardown(self):
        super(TestAvlBase, self).teardown()
        self.avl.disconnect()

    def test_hello_world(self):
        pass
