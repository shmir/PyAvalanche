"""
Classes and utilities to manage Avalanche project.
"""

from avalanche.avl_object import AvlObject


class AvlProject(AvlObject):
    """ Represents Avalanche project object. """

    def __init__(self, **data):
        super(self.__class__, self).__init__(objType='project', **data)
        self.get_children('tests')

    @property
    def tests(self):
        return self.get_objects_by_type('test')


class AvlTest(AvlObject):
    """ Represents Avalanche test object. """

    def __init__(self, **data):
        super(self.__class__, self).__init__(**data)
        self.client = self.get_child('configuration.test.client')
        self.server = self.get_child('configuration.test.server')


class AvlCluster(AvlObject):
    """ Represents Avalanche cluster. """

    pass


class AvlClient(AvlCluster):
    """ Represents Avalanche client side. """

    def __init__(self, **data):
        super(self.__class__, self).__init__(**data)
        self.associations = self.get_child('globalassociations.association', 'userbasedassociations.association')


class AvlServer(AvlCluster):
    """ Represents Avalanche server side. """

    def __init__(self, **data):
        super(self.__class__, self).__init__(**data)
        self.associations = self.get_child('association')


class AvlAssociation(AvlObject):
    """ Represents Avalanche association. """

    def get_name(self):
        return int(self.get_attribute('id')) + 1
