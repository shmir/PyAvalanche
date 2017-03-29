"""
This module implements classes and utility functions to manage Avalanche HW.

:author: yoram@ignissoft.com
"""

from collections import OrderedDict

from avalanche.avl_object import AvlObject


class StcHw(AvlObject):
    """ Represent STC physical chassis manager. """

    pass


class AvlPhyBase(AvlObject):
    """ Base class for all Avalanche Physical sub-tree objects. """

    def get_inventory(self):
        self.attributes = self.get_attributes(*self.attributes_names)
        for child_var, child_type_name in self.children_types.items():
            child_type, child_name = child_type_name
            children = OrderedDict()
            for child in self.get_objects_or_children_by_type(child_type):
                children[child_name + child.get_attribute('Index')] = child
            setattr(self, child_var, children)
            for child in getattr(self, child_var).values():
                child.get_inventory()


class AvlPhyChassis(AvlPhyBase):
    """ Represent STC physical chassis. """

    attributes_names = ('Model', 'SerialNum')
    children_types = {'modules': ('PhysicalTestModule', 'Slot ')}

    def get_module_by_index(self, index):
        for module in self.modules.values():
            if module.attributes['Index'] == index:
                return module


class AvlPhyModule(AvlPhyBase):

    attributes_names = ('Index', 'Model', 'Description', 'SerialNum', 'FirmwareVersion')
    children_types = {'ports': ('PhysicalPort', 'Port ')}


class AvlPhyPort(AvlPhyBase):

    attributes_names = ('Index',)
    children_types = {}

    def get_supported_speeds(self):
        pass
