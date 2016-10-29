#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
test_zeus_client
----------------------------------

Tests for `zeus` module.
"""

import json
import mock
import unittest
from zeus.interfaces.utils import validateDates, ZeusException

from zeus import client

FAKE_TOKEN = 'ZeUsRoCkS'
FAKE_SERVER = 'https://zeus.rocks'


class TestZeusClient(unittest.TestCase):

    def setUp(self):
        # Setting up a Zeus client with a fake token:
        self.z = client.ZeusClient(FAKE_TOKEN, FAKE_SERVER)

    def test_initialization_no_https(self):
        z = client.ZeusClient(FAKE_TOKEN, "zeus.rocks")
        assert z.server == "https://zeus.rocks"
        z = client.ZeusClient(FAKE_TOKEN, "http://zeus.rocks")
        assert z.server == "https://zeus.rocks"

    def test_validate_dates(self):
        # normal
        from_date = 12345
        to_date = 12346
        validateDates(from_date, to_date)
        # None value
        from_date = None
        to_date = 12346
        validateDates(from_date, to_date)
        # invalid value
        from_date = 'wrongvalue'
        to_date = 12346
        self.assertRaises(
            ZeusException, validateDates, from_date, to_date)
        # inversed order
        from_date = 12346
        to_date = 12345
        self.assertRaises(
            ZeusException, validateDates, from_date, to_date)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_post_empty_log(self, mock_requests):
        logs = []
        self.z.sendLog('ZeusTest', logs)
        mock_requests.post.assert_called_with(FAKE_SERVER + '/logs/' +
                                              FAKE_TOKEN + '/ZeusTest/',
                                              data={"logs": json.dumps(logs)},
                                              headers=None)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_post_single_log(self, mock_requests):
        logs = [{"timestamp": 123541423, "key": "TestLog", "key2": 123}]
        self.z.sendLog('ZeusTest', logs)
        mock_requests.post.assert_called_with(FAKE_SERVER + '/logs/' +
                                              FAKE_TOKEN + '/ZeusTest/',
                                              data={"logs": json.dumps(logs)},
                                              headers=None)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_post_single_log_wrong_name(self, mock_requests):
        logs = [{"message": "TestLog", "value": 23}]
        self.assertRaises(
            ZeusException, self.z.sendLog, 'W.rongName', logs)
        self.assertRaises(
            ZeusException, self.z.sendLog, '_WrongName', logs)
        self.assertRaises(
            ZeusException, self.z.sendLog, 'W#?rongName', logs)
        self.assertRaises(
            ZeusException, self.z.sendLog, 'W-rongName', logs)
        self.assertRaises(
            ZeusException, self.z.sendLog, None, logs)
        self.assertRaises(
            ZeusException, self.z.sendLog, '', logs)
        self.assertRaises(
            ZeusException, self.z.sendLog, '0123456789ABCDEF' * 16,
            logs)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_post_multiple_logs(self, mock_requests):
        logs = [{"timestamp": 123541423, "message": "TestLog"},
                {"timestamp": 123541424, "message": "TestLog2"},
                {"timestamp": 123541425, "message": "TestLog3"}, ]
        self.z.sendLog('ZeusTest', logs)
        mock_requests.post.assert_called_with(FAKE_SERVER + '/logs/' +
                                              FAKE_TOKEN + '/ZeusTest/',
                                              data={"logs": json.dumps(logs)},
                                              headers=None)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_get_logs(self, mock_requests):
        self.z.getLog('ZeusTest',
                      attribute_name='message',
                      pattern='*',
                      from_date=123456789,
                      to_date=126235344235,
                      offset=23,
                      limit=10)
        mock_requests.get.assert_called_with(FAKE_SERVER + '/logs/' +
                                             FAKE_TOKEN + '/',
                                             params={'log_name': 'ZeusTest',
                                                     'attribute_name':
                                                     'message',
                                                     'pattern': '*',
                                                     'from': 123456789,
                                                     'to': 126235344235,
                                                     'offset': 23,
                                                     'limit': 10})

    @mock.patch('zeus.interfaces.rest.requests')
    def test_post_empty_metric(self, mock_requests):
        metrics = []
        self.z.sendMetric('ZeusTest', metrics)
        mock_requests.post.assert_called_with(FAKE_SERVER + '/metrics/' +
                                              FAKE_TOKEN + '/ZeusTest/',
                                              data={"metrics":
                                                    json.dumps(metrics)},
                                              headers=None)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_post_single_metric(self, mock_requests):
        metrics = [{"timestamp": 123541423, "value": 0}]
        self.z.sendMetric('Zeus.Test', metrics)
        mock_requests.post.assert_called_with(FAKE_SERVER + '/metrics/' +
                                              FAKE_TOKEN + '/Zeus.Test/',
                                              data={"metrics":
                                                    json.dumps(metrics)},
                                              headers=None)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_post_single_metric_wrong_name(self, mock_requests):
        metrics = [{"timestamp": 123541423, "value": 0}]
        self.assertRaises(
            ZeusException, self.z.sendMetric, '_WrongName', metrics)
        self.assertRaises(
            ZeusException, self.z.sendMetric, 'W#?rongName', metrics)
        self.assertRaises(
            ZeusException, self.z.sendMetric, None, metrics)
        self.assertRaises(
            ZeusException, self.z.sendMetric, '', metrics)
        self.assertRaises(
            ZeusException, self.z.sendMetric, '0123456789ABCDEF' * 16,
            metrics)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_post_multiple_metrics(self, mock_requests):
        metrics = [{"timestamp": 123541423, "value": 0},
                   {"timestamp": 123541424, "value": 1},
                   {"timestamp": 123541425, "value": 2.0}, ]
        self.z.sendMetric('ZeusTest', metrics)
        mock_requests.post.assert_called_with(FAKE_SERVER + '/metrics/' +
                                              FAKE_TOKEN + '/ZeusTest/',
                                              data={"metrics":
                                                    json.dumps(metrics)},
                                              headers=None)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_get_metric_values(self, mock_requests):
        self.z.getMetric(metric_name='ZeusTest',
                         aggregator_function='sum',
                         aggregator_column='val1',
                         from_date=123456789,
                         to_date=126235344235,
                         group_interval='1m',
                         filter_condition='value > 90',
                         limit=10,
                         offset=20)
        mock_requests.get.assert_called_with(FAKE_SERVER + '/metrics/' +
                                             FAKE_TOKEN + '/_values/',
                                             params={'metric_name': 'ZeusTest',
                                                     'aggregator_function':
                                                     'sum',
                                                     'aggregator_column':
                                                     'val1',
                                                     'from': 123456789,
                                                     'to': 126235344235,
                                                     'group_interval': '1m',
                                                     'filter_condition':
                                                     'value > 90',
                                                     'limit': 10,
                                                     'offset': 20})

    @mock.patch('zeus.interfaces.rest.requests')
    def test_get_metric_names(self, mock_requests):
        self.z.getMetricNames(metric_name='ZeusTest',
                              limit=10,
                              offset=20)
        mock_requests.get.assert_called_with(FAKE_SERVER + '/metrics/' +
                                             FAKE_TOKEN + '/_names/',
                                             params={'metric_name': 'ZeusTest',
                                                     'limit': 10,
                                                     'offset': 20})

    @mock.patch('zeus.interfaces.rest.requests')
    def test_get_delete_metric(self, mock_requests):
        self.z.deleteMetric('ZeusTest')
        mock_requests.delete.assert_called_with(FAKE_SERVER + '/metrics/' +
                                                FAKE_TOKEN + '/ZeusTest/')

    @mock.patch('zeus.interfaces.rest.requests')
    def test_get_delete_metric_wrong_name(self, mock_requests):
        self.assertRaises(
            ZeusException, self.z.deleteMetric, '_WrongName')

    @mock.patch('zeus.interfaces.rest.requests')
    def tearDown(self, mock_requests):
        pass

if __name__ == '__main__':
    unittest.main()
