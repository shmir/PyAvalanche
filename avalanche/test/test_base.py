"""
Base class for all Avalanche package tests.

@author yoram@ignissoft.com
"""

from os import path

from trafficgenerator.test.test_tgn import TgnTest

from avalanche.avl_app import init_avl


class AvlTestBase(TgnTest):

    TgnTest.config_file = path.join(path.dirname(__file__), 'Avalanche.ini')

    def setUp(self):
        super(AvlTestBase, self).setUp()
        self.avl = init_avl(self.logger, self.config.get('Tcl', 'install_dir'), self.config.get('AVL', 'install_dir'))
        self.avl.connect()

    def tearDown(self):
        super(AvlTestBase, self).tearDown()
        self.avl.disconnect()

    def testHelloWorld(self):
        pass
