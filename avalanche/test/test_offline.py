"""
Avalanche package tests that can run in offline mode.

@author yoram@ignissoft.com
"""

from os import path

from avalanche.test.test_base import AvlTestBase


class AvlTestOffline(AvlTestBase):

    def test_load_config(self):
        """ Load existing configuration. """
        self.logger.info(AvlTestOffline.test_load_config.__doc__.strip())

        self.avl.load_config(path.join(path.dirname(__file__), 'configs/test_config.spf'))
        file_name, file_ext = path.splitext(path.join(path.dirname(__file__), 'configs/test_config.spf'))
        self.avl.save_config(file_name + '_save' + file_ext)

    def test_analyze_config(self):
        """ Analyze existing configuration. """
        self.logger.info(AvlTestOffline.test_analyze_config.__doc__.strip())

        self.avl.load_config(path.join(path.dirname(__file__), 'configs/test_config.spf'))
        assert(len(self.avl.project.tests) == 3)
