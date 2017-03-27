"""
TestCenter package tests that can run in offline mode.

@author yoram@ignissoft.com
"""

from os import path
import inspect

from avalanche.stc_object import StcObject
from avalanche.stc_port import StcPort
from avalanche.stc_device import StcDevice
from avalanche.stc_stream import StcStream

from avalanche.test.test_base import StcTestBase


class StcTestOffline(StcTestBase):

    def testLoadConfig(self):
        """ Load existing configuration. """
        self.logger.info(StcTestOffline.testLoadConfig.__doc__.strip())

        self.stc.load_config(path.join(path.dirname(__file__), 'configs/test_config.tcc'))
        file_name, file_ext = path.splitext(path.join(path.dirname(__file__), 'configs/test_config.tcc'))
        self.stc.save_config(file_name + '-save' + file_ext)

        self.assertRaises(Exception, self.stc.load_config, path.join(path.dirname(__file__), 'tcc.invalid'))
        self.assertRaises(Exception, self.stc.load_config, path.join(path.dirname(__file__), 'invalid.tcc'))

        pass

    def testAnalyzeConfig(self):
        """ Analyze existing configuration. """
        self.logger.info(StcTestOffline.testAnalyzeConfig.__doc__.strip())

        self.stc.load_config(path.join(path.dirname(__file__), 'configs/test_config.tcc'))
        project = self.stc.project

        project.get_children('port')
        port1_obj = project.get_object_by_name('Port 1')

        print('Port1 object reference = ', port1_obj.obj_ref())
        print('Port1 name = ', port1_obj.obj_name())
        print('Ports = ', project.get_objects_by_type('port'))
        print('Port 1 state = ', port1_obj.get_attribute('Location'))
        print('Port 1 attributes = ', port1_obj.get_attributes())
        print('Port 1 streamblocks = ', port1_obj.get_children('streamblock'))
        print('Port 2 streamblocks = ', port1_obj.get_children('streamblock'))

        stc_ports = project.get_children('port')
        assert(len(stc_ports) == 2)

        assert(len(stc_ports[0].get_children('emulateddevice')) == 1)
        assert(len(stc_ports[1].get_children('emulateddevice')) == 1)

        assert(len(self.stc.project.get_devices()) == 2)
        assert(len(self.stc.project.get_devices(stc_ports[0])) == 1)
        assert(len(self.stc.project.get_devices(stc_ports[1])) == 1)

        assert(len(self.stc.project.get_children('GroupCollection')) == 1)
        assert(len(self.stc.project.get_object_by_name('TG 1').get_children('TrafficGroup')) == 1)
        assert(len(self.stc.project.get_object_by_name('TG 1').get_object_by_name('SG 1').get_stream_blocks()) == 2)
        assert(len(self.stc.project.get_stream_blocks()) == 2)

        pass

    def testChildren(self):
        """ Test specific get children methods. """
        self.logger.info(StcTestOffline.testChildren.__doc__)

        self.stc.load_config(path.join(path.dirname(__file__), 'configs/test_config.tcc'))
        project = self.stc.project

        ports = project.get_ports()
        assert(len(ports) == 2)
        for port in ports.values():
            assert(len(port.get_devices()) == 1)
            assert(len(port.get_stream_blocks()) == 1)

    def testBuildConfig(self):
        """ Build simple config from scratch. """
        self.logger.info(StcTestOffline.testBuildConfig.__doc__.strip())

        for port_name in ('Port 1', 'Port 2'):
            self.logger.info('Create Port "%s"', port_name)
            stc_port = StcPort(name=port_name)

            for dev_name in (port_name + ' Device 1', port_name + ' Device 2'):
                self.logger.info('Build Device "%s"', dev_name)
                stc_dev = StcDevice(name=dev_name, parent=stc_port)
                stc_eth = StcObject(objType='EthIIIf', parent=stc_dev)
                stc_eth.set_attributes(SourceMac='00:11:22:33:44:55')
                stc_ip = StcObject(objType='Ipv4If', parent=stc_dev)
                stc_ip.set_attributes(Address='1.2.3.4', PrefixLength=16)

            for sb_name in (port_name + ' StreamBlock 1', port_name + ' StreamBlock 2'):
                self.logger.info('Build StreamBlock "%s"', sb_name)
                stc_sb = StcStream(name=sb_name, parent=stc_port)
                stc_eth = StcObject(objType='ethernet:ethernetii', parent=stc_sb)
                stc_eth.set_attributes(DstMac='00:10:20:30:40:50')

        stc_ports = self.stc.project.get_children('port')
        assert(len(stc_ports) == 2)
        for stc_port in stc_ports:
            assert(len(stc_port.get_children('generator')) == 1)
            assert(len(stc_port.get_children('generator', 'analyzer')) == 2)
            assert(len(stc_port.get_children('emulateddevice')) == 2)
            assert(len(stc_port.get_children('emulateddevice', 'generator', 'analyzer')) == 4)
        for stc_port in stc_ports:
            assert(len(stc_port.get_children('streamblock')) == 2)

        test_name = inspect.stack()[0][3]
        self.stc.save_config(path.join(path.dirname(__file__), 'configs', test_name + '.tcc'))

        pass

    def testBuildEmulation(self):
        """ Build simple BGP configuration. """
        self.logger.info(StcTestOffline.testBuildEmulation.__doc__.strip())

        stc_port = StcPort(name='Port 1')
        stc_dev = StcDevice(name='Device 1', parent=stc_port)
        stc_eth = StcObject(objType='EthIIIf', parent=stc_dev)
        stc_eth.set_attributes(SourceMac='00:11:22:33:44:55')
        stc_ip = StcObject(objType='Ipv4If', parent=stc_dev)
        stc_ip.set_attributes(Address='1.2.3.4', PrefixLength=16)
        stc_bgp = StcObject(objType='BgpRouterConfig', parent=stc_dev)

        test_name = inspect.stack()[0][3]
        self.stc.save_config(path.join(path.dirname(__file__), 'configs', test_name + '.tcc'))

        pass
