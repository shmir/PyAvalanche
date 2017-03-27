"""
Base class for all STC package tests.

@author yoram@ignissoft.com
"""

from os import path

from trafficgenerator.test.test_tgn import TgnTest
from trafficgenerator.tgn_tcl import TgnTkMultithread

from avalanche.api.avl_tcl import AvlTclWrapper
from avalanche.avl_app import StcApp


class AvlTestBase(TgnTest):

    tcl_interp = None
    stc = None

    TgnTest.config_file = path.join(path.dirname(__file__), 'Avalanche.ini')

    def setUp(self):
        super(AvlTestBase, self).setUp()
        api_wrapper = AvlTclWrapper(self.logger, self.config.get('AVL', 'install_dir'))
#         self.avl = StcApp(self.logger, api_wrapper=api_wrapper)
#         log_level = self.config.get('AVL', 'log_level')
#         self.stc.system.get_child('automationoptions').set_attributes(LogLevel=log_level)
#         self.stc.connect()

    def tearDown(self):
        super(AvlTestBase, self).tearDown()
        self.stc.disconnect()
        if self.tcl_interp:
            self.tcl_interp.stop()

    def testHelloWorld(self):
        pass
