import mock

from zabbix_base_action_test_case import ZabbixBaseActionTestCase
from call_api import CallAPI


class CallAPITest(ZabbixBaseActionTestCase):
    __test__ = True
    action_cls = CallAPI

    @mock.patch('lib.actions.ZabbixBaseAction.connect')
    def test_run_action_without_token(self, mock_conn):
        action = self.get_action_instance(self.full_config)

        # This is a mock of calling API 'hoge'
        action.client = mock.Mock()
        action.client.hoge.return_value = 'result'

        # This checks that a method which is specified in the api_method parameter would be called
        self.assertEqual(action.run(api_method='hoge', token=None, param='foo'), 'result')

    @mock.patch('call_api.ZabbixAPI')
    def test_run_action_with_token(self, mock_client):
        action = self.get_action_instance(self.full_config)

        # This is a mock of calling API 'hoge' to confirm that
        # specified parameters would be passed correctly.
        def side_effect(*args, **kwargs):
            return (args, kwargs)

        _mock_client = mock.Mock()
        _mock_client.hoge.side_effect = side_effect
        mock_client.return_value = _mock_client

        # This checks that specified parameter and access token would be set expectedly
        result = action.run(api_method='hoge', token='test_token', param='foo')
        self.assertEqual(result, ((), {'param': 'foo'}))
        self.assertEqual(action.auth, 'test_token')
