"""
Classes and utilities to manage STC statistics views.
"""

from collections import OrderedDict

from trafficgenerator.tgn_tcl import tcl_list_2_py_list
from avalanche.avl_object import AvlObject


class AvlStats(object):
    """ Represents statistics view. """

    statistics = {}

    def __init__(self, project, side, view):
        """ Subscribe to view with default configuration type as defined by config_2_type.

        :param project: parent project object for all statistics.
        :param side: client/server.
        :param view: statistics view to subscribe to.
        """

        super(AvlStats, self).__init__()
        self.project = project
        if view:
            self.subscribe(side, view)
        self.statistics = OrderedDict()

    def subscribe(self, side, view):
        """ Subscribe to statistics view.

        :param side: client/server.
        :param view: statistics view to subscribe to.
        """

        rds = self.project.api.avl_command('subscribe', side, '"{}* all"'.format(view))
        self.rds = AvlObject(ObjType='ResultDataSet', parent=self.project, objRef=rds)
#         self.rdo = self.rds.get_child('resultdataobjects')

    def unsubscribe(self):
        """ UnSubscribe from statistics view. """

        self.project.api.unsubscribe(self.rds.ref)

    def read_stats(self):
        """ Reads the statistics view from Avalanche and saves it in statistics dictionary. """

#         self.statistcs = self.rdo.get_attributes()
        raw_stats = self.project.api.avl_command('perform getValues {}'.format(self.rds.ref))
        if raw_stats != '{Values {}}':
            for sample_num in tcl_list_2_py_list(raw_stats[9:-2]):
                timestamp, stats = tcl_list_2_py_list(sample_num)
                self.statistics[timestamp] = {key_val.split()[0]: key_val.split()[1] for
                                              key_val in tcl_list_2_py_list(stats)}


class AvlClientStats(AvlStats):

    def __init__(self, project, view):
        """ Subscribe to client view.

        :param project: parent project object for all statistics.
        :param view: client statistics view to subscribe to.
        """
        super(AvlClientStats, self).__init__(project, 'client', view)


class AvlServerStats(AvlStats):

    def __init__(self, project, view):
        """ Subscribe to server view.

        :param project: parent project object for all statistics.
        :param view: server statistics view to subscribe to.
        """

        super(AvlClientStats, self).__init__(project, 'server', view)
