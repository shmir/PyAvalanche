"""
Classes and utilities to manage Avalanche project.
"""

from avalanche.avl_object import AvlObject


class AvlProject(AvlObject):
    """ Represents Avalanche project object. """

    def __init__(self, **data):
        super(AvlProject, self).__init__(objType='project', **data)
