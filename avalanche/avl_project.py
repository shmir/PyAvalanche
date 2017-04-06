"""
Classes and utilities to manage Avalanche project.
"""

from avalanche.avl_object import AvlObject


class AvlProject(AvlObject):
    """ Represents Avalanche project object. """

    def __init__(self, **data):
        super(self.__class__, self).__init__(objType='project', **data)
        self.get_children('tests')

    def get_tests(self):
        return self.get_objects_by_type('test')


class AvlTest(AvlObject):
    """ Represents Avalanche test object. """

    def __init__(self, **data):
        super(self.__class__, self).__init__(**data)
        self.client = self.get_child('configuration.test.client')
        self.server = self.get_child('configuration.test.server')

    pass


class AvlServer(AvlObject):
    """ Represents Avalanche test object. """

    def __init__(self, **data):
        super(self.__class__, self).__init__(**data)
        self.get_child('association')

    pass
