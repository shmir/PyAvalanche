"""
Classes and utilities to manage Avalanche HW.

:author: yoram@ignissoft.com
"""

from collections import OrderedDict

from avalanche.avl_object import AvlObject


class AvlPhyBase(AvlObject):
    """ Base class for all Avalanche Physical sub-tree objects. """

    def get_inventory(self):
        self.attributes = self.get_attributes(*self.attributes_names)
        for child_var, child_type_index in self.children_types.items():
            child_type, child_index = child_type_index
            children = OrderedDict()
            for child in self.get_children(child_type):
                children[child.get_attribute(child_index)] = child
            setattr(self, child_var, children)
            for child in getattr(self, child_var).values():
                child.get_inventory()


class AvlHw(AvlPhyBase):

    chassis = OrderedDict()

    def get_port(self, location):
        chassis, module, port = location.split('/')
        return self.chassis[chassis].modules[module].ports[port]


class AvlChassis(AvlPhyBase):
    """ Represent Avalanche physical chassis/appliance. """

    attributes_names = ('ActiveSoftware', 'Model', 'SerialNumber')
    children_types = {'modules': ('PhysicalTestModules', 'SlotNumber')}


class AvlModule(AvlPhyBase):

    attributes_names = ()
    children_types = {'ports': ('Ports', 'PortNumber')}


class AvlPort(AvlPhyBase):

    attributes_names = ('Location',)
    children_types = {}

    def reserve(self):
        self.api.avl_command('reserve', self.attributes['Location'])

    def release(self):
        self.api.avl_command('release', self.attributes['Location'])
