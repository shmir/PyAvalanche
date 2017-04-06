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


class AvlChassis(AvlPhyBase):
    """ Represent Avalanche physical chassis/appliance. """

    attributes_names = ('ActiveSoftware', 'Model', 'SerialNumber')
    children_types = {'modules': ('PhysicalTestModules', 'SlotNumber')}

    def get_module_by_index(self, index):
        for module in self.modules.values():
            if module.attributes['SlotNumber'] == index:
                return module


class AvlModule(AvlPhyBase):

    attributes_names = ()
    children_types = {'ports': ('Ports', 'PortNumber')}


class AvlPort(AvlPhyBase):

    attributes_names = ()
    children_types = {}
