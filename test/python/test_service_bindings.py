import httplib
import unittest

import mock

from abstract_test_case import AbstractTestCase
from fake_requests import mock_response


class TestServiceBindings(unittest.TestCase, AbstractTestCase):
    def setUp(self):
        self.build_client()

    def test_list(self):
        self.client.get.return_value = mock_response(
            '/v2/service_bindings?q=service_instance_guid%20IN%20instance_guid',
            httplib.OK,
            None,
            'v2', 'service_bindings', 'GET_response.json')
        cpt = reduce(lambda increment, _: increment + 1,
                     self.client.service_binding.list(service_instance_guid='instance_guid'), 0)
        self.client.get.assert_called_with(self.client.get.return_value.url)
        self.assertEqual(cpt, 1)

    def test_get(self):
        self.client.get.return_value = mock_response(
            '/v2/service_bindings/service_binding_id',
            httplib.OK,
            None,
            'v2', 'service_bindings', 'GET_{id}_response.json')
        result = self.client.service_binding.get('service_binding_id')
        self.client.get.assert_called_with(self.client.get.return_value.url)
        self.assertIsNotNone(result)

    def test_create(self):
        self.client.post.return_value = mock_response(
            '/v2/service_bindings',
            httplib.CREATED,
            None,
            'v2', 'service_bindings', 'POST_response.json')
        service_bindiing = self.client.service_binding.create('app_guid', 'instance_guid',
                                                              dict(the_service_broker='wants this object'))
        self.client.post.assert_called_with(self.client.post.return_value.url,
                                            json=dict(app_guid='app_guid',
                                                      service_instance_guid='instance_guid',
                                                      parameters=dict(
                                                          the_service_broker='wants this object')))
        self.assertIsNotNone(service_bindiing)

    def test_delete(self):
        self.client.delete.return_value = mock_response(
            '/v2/service_bindings/binding_id',
            httplib.NO_CONTENT,
            None)
        self.client.service_binding.remove('binding_id')
        self.client.delete.assert_called_with(self.client.delete.return_value.url)

    def test_entity(self):
        self.client.get.side_effect = [
            mock_response(
                '/v2/service_bindings/service_binding_id',
                httplib.OK,
                None,
                'v2', 'service_bindings', 'GET_{id}_response.json'),
            mock_response(
                '/v2/service_instances/ef0bf611-82c6-4603-99fc-3a1a893109d0',
                httplib.OK,
                None,
                'v2', 'service_instances', 'GET_{id}_response.json'),
            mock_response(
                '/v2/apps/c77953c8-6c35-46c7-816e-cf0c42ac2f52',
                httplib.OK,
                None,
                'v2', 'apps', 'GET_{id}_response.json')
        ]
        service_binding = self.client.service_binding.get('service_binding_id')
        self.assertIsNotNone(service_binding.service_instance())
        self.assertIsNotNone(service_binding.application())
        self.client.get.assert_has_calls([mock.call(side_effect.url) for side_effect in self.client.get.side_effect],
                                         any_order=False)
