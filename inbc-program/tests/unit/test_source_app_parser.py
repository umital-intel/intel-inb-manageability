from unittest import TestCase
from unittest.mock import patch

from inbc.inbc import Inbc
from inbc.parser.parser import ArgsParser


class TestSourceApplicationParser(TestCase):
    def setUp(self):
        self.arg_parser = ArgsParser()
        self.maxDiff = None

    def test_parse_add_arguments_successfully(self):
        f = self.arg_parser.parse_args(
            ['source', 'application', 'add',
             '--gpgKeyUri', 'https://repositories.intel.com/gpu/intel-graphics.key',
             '--gpgKeyName', 'intel-graphics.gpg',
             '--sources', 'deb http://example.com/ focal main restricted universe',
             'deb-src http://example.com/ focal-security main',
             '--filename', 'intel-gpu-jammy.list'])
        self.assertEqual(f.gpgKeyUri, 'https://repositories.intel.com/gpu/intel-graphics.key')
        self.assertEqual(f.gpgKeyName, 'intel-graphics.gpg')
        self.assertEqual(f.sources, ['deb http://example.com/ focal main restricted universe',
                                     'deb-src http://example.com/ focal-security main'])
        self.assertEqual(f.filename, 'intel-gpu-jammy.list')

    @patch('inbm_lib.mqttclient.mqtt.mqtt.Client.connect')
    def test_create_add_manifest_successfully(self, m_connect):
        p = self.arg_parser.parse_args(
            ['source', 'application', 'add',
             '--gpgKeyUri', 'https://repositories.intel.com/gpu/intel-graphics.key',
             '--gpgKeyName', 'intel-graphics.gpg',
             '--sources', 'deb http://example.com/ focal main restricted universe',
             'deb-src http://example.com/ focal-security main',
             '--filename', 'intel-gpu-jammy.list'])
        Inbc(p, 'source', False)
        expected = '<?xml version="1.0" encoding="utf-8"?><manifest><type>source</type><applicationSource>' \
                   '<add><gpg><uri>https://repositories.intel.com/gpu/intel-graphics.key</uri>' \
                   '<keyname>intel-graphics.gpg</keyname></gpg><repo><repos>' \
                   '<source_pkg>deb http://example.com/ focal main restricted universe</source_pkg>' \
                   '<source_pkg>deb-src http://example.com/ focal-security main</source_pkg>' \
                   '</repos><filename>intel-gpu-jammy.list</filename></repo></add></applicationSource></manifest>'
        self.assertEqual(p.func(p), expected)

    def test_parse_remove_arguments_successfully(self):
        f = self.arg_parser.parse_args(
            ['source', 'application', 'remove',
             '--gpgKeyName', 'intel-gpu-jammy.gpg',
             '--filename', 'intel-gpu-jammy.list'])
        self.assertEqual(f.gpgKeyName, 'intel-gpu-jammy.gpg')
        self.assertEqual(f.filename, 'intel-gpu-jammy.list')

    @patch('inbm_lib.mqttclient.mqtt.mqtt.Client.connect')
    def test_create_remove_manifest_successfully(self, m_connect):
        p = self.arg_parser.parse_args(
            ['source', 'application', 'remove',
             '--gpgKeyName', 'intel-gpu-jammy.gpg',
             '--filename', 'intel-gpu-jammy.list'])
        Inbc(p, 'source', False)
        expected = '<?xml version="1.0" encoding="utf-8"?><manifest><type>source</type><applicationSource>' \
                   '<remove><gpg><keyname>intel-gpu-jammy.gpg</keyname></gpg>' \
                   '<repo><filename>intel-gpu-jammy.list</filename></repo></remove></applicationSource></manifest>'
        self.assertEqual(p.func(p), expected)

    def test_parse_update_arguments_successfully(self):
        f = self.arg_parser.parse_args(
            ['source', 'application', 'update',
             '--sources', 'deb http://example.com/ focal main restricted universe',
             'deb-src http://example.com/ focal-security main',
             '--filename', 'intel-gpu-jammy.list'])
        self.assertEqual(f.sources, ['deb http://example.com/ focal main restricted universe',
                                     'deb-src http://example.com/ focal-security main'])
        self.assertEqual(f.filename, 'intel-gpu-jammy.list')

    @patch('inbm_lib.mqttclient.mqtt.mqtt.Client.connect')
    def test_create_update_manifest_successfully(self, m_connect):
        p = self.arg_parser.parse_args(
            ['source', 'application', 'update',
             '--sources', 'deb http://example.com/ focal main restricted universe',
             'deb-src http://example.com/ focal-security main',
             '--filename', 'intel-gpu-jammy.list'])
        Inbc(p, 'source', False)
        expected = '<?xml version="1.0" encoding="utf-8"?><manifest><type>source</type><applicationSource>' \
                   '<update><repo><repos><source_pkg>deb http://example.com/ focal main restricted universe' \
                   '</source_pkg><source_pkg>deb-src http://example.com/ focal-security main</source_pkg>' \
                   '</repos><filename>intel-gpu-jammy.list</filename></repo></update></applicationSource></manifest>'
        self.assertEqual(p.func(p), expected)

    @patch('inbm_lib.mqttclient.mqtt.mqtt.Client.connect')
    def test_create_list_manifest_successfully(self, m_connect):
        p = self.arg_parser.parse_args(
            ['source', 'application', 'list'])
        Inbc(p, 'source', False)
        expected = '<?xml version="1.0" encoding="utf-8"?><manifest><type>source</type><applicationSource>' \
                   '<list/></applicationSource></manifest>'
        self.assertEqual(p.func(p), expected)
