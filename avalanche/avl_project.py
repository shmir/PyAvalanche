"""
Classes and utilities to manage Avalanche project.
"""

import time

from avalanche.avl_object import AvlObject


class AvlProject(AvlObject):
    """ Represents Avalanche project object. """

    def __init__(self, **data):
        super(self.__class__, self).__init__(objType='project', **data)
        self.get_children('tests')

    def new_test(self, name='Test', testtype='deviceComplex'):
        """ Create new test. """

        test_ref = self.api.avl_command('createTest', project=self.ref, test=name, type=testtype)
        AvlTest(parent=self, objRef=test_ref, name=name)
        return self.tests[name]

    @property
    def tests(self):
        return {test.name: test for test in self.get_objects_by_type('test')}


class AvlTest(AvlObject):
    """ Represents Avalanche test object. """

    def __init__(self, **data):
        data['objType'] = 'test'
        super(self.__class__, self).__init__(**data)
        self.topology = self.get_child('configuration.topology')
        self.client = self.get_child('configuration.test.client')
        self.server = self.get_child('configuration.test.server')

    def start(self, trial=False, blocking=False):
        self.system.api.avl_command('apply', self.ref, '1' if trial else '0', '1')
        status = self.status()
        while status != 'TEST_RUNNING' and status != 'TEST_COMPLETED':
            time.sleep(1)
            status = self.status()
        if blocking:
            self.wait()

    def stop(self):
        self.command('stop {}'.format(self.system.ref), workspace=self.system.get_attribute('workspace'))
        self.wait()

    def wait(self):
        status = self.status()
        while status != 'TEST_COMPLETED':
            time.sleep(1)
            status = self.status()

    def status(self):
        return self.system.get_objects_or_children_by_type('runningtestinfo')[0].get_attribute('runningTestStatus')


class AvlCluster(AvlObject):
    """ Represents Avalanche cluster. """

    pass


class AvlClient(AvlCluster):
    """ Represents Avalanche client side. """

    def __init__(self, **data):
        super(self.__class__, self).__init__(**data)
        self.associations = self.get_children('globalassociations.association', 'userbasedassociations.association')


class AvlServer(AvlCluster):
    """ Represents Avalanche server side. """

    def __init__(self, **data):
        super(self.__class__, self).__init__(**data)
        self.associations = self.get_children('association')


class AvlAssociation(AvlObject):
    """ Represents Avalanche association. """

    def __init__(self, **data):
        self.associated_interface = data.pop('associated_interface', None)
        self.association_type = data.pop('association_type', None)
        data['objType'] = 'association'
        super(self.__class__, self).__init__(**data)
        self.interface = self.get_child('associated_interface')

    def _create(self):
        """ Create new association on Avalanche.

        @return: association object reference.
        """

        # At this time objRef is not set yet so we must use direct calls to api.
        parent = self.parent.ref
        if self.association_type:
            parent += '.' + self.association_type
        return self.api.create('association', parent, associated_interface=self.associated_interface)

    def get_name(self):
        return int(self.get_attribute('id')) + 1


class AvlInterface(AvlObject):
    """ Represents Avalanche interface. """

    def __init__(self, **data):
        self.side = data.pop('side', None)
        data['objType'] = 'interface'
        super(self.__class__, self).__init__(**data)

    def _create(self):
        """ Create new interface on Avalanche.

        @return: interface object reference.
        """

        # At this time objRef is not set yet so we must use direct calls to api.
        obj_ref = super(self.__class__, self)._create()
        self.api.config(obj_ref, side=self.side)
        return obj_ref

    def set_port(self, location):
        self.set_attributes(port=location)
