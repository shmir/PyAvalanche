"""
Base class for all STC package tests.

@author yoram@ignissoft.com
"""

from os import path

from trafficgenerator.test.test_tgn import TgnTest

from avalanche.api.avl_tcl import AvlTclWrapper
from avalanche.avl_app import AvlApp


class AvlTestBase(TgnTest):

    tcl_interp = None
    stc = None

    TgnTest.config_file = path.join(path.dirname(__file__), 'Avalanche.ini')

    def setUp(self):
        super(AvlTestBase, self).setUp()
        api_wrapper = AvlTclWrapper(self.logger, self.config.get('Tcl', 'install_dir'),
                                    self.config.get('AVL', 'install_dir'))
        self.avl = AvlApp(self.logger, api_wrapper=api_wrapper)
        self.avl.connect(self.config.get('AVL', 'chassis'))

    def tearDown(self):
        super(AvlTestBase, self).tearDown()
        self.avl.disconnect()
        if self.tcl_interp:
            self.tcl_interp.stop()

    def testHelloWorld(self):
        pass
