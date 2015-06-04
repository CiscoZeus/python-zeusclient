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

from zeus import client

FAKE_TOKEN = 'ZeUsRoCkS'
FAKE_SERVER = 'http://zeus.rocks'


class TestZeusClient(unittest.TestCase):

    def setUp(self):
        # Setting up a Zeus client with a fake token:
        self.z = client.ZeusClient(FAKE_TOKEN, FAKE_SERVER)

    def test_initialization_no_http(self):
        z = client.ZeusClient(FAKE_TOKEN, "zeus.rocks")
        assert z.server == "http://zeus.rocks"

    @mock.patch('zeus.client.requests')
    def test_post_empty_log(self, mock_requests):
        logs = []
        self.z.sendLog('ZeusTest', logs)
        mock_requests.post.assert_called_with(FAKE_SERVER + '/logs/' +
                                              FAKE_TOKEN + '/ZeusTest/',
                                              data={"logs": json.dumps(logs)})

    @mock.patch('zeus.client.requests')
    def test_post_single_log(self, mock_requests):
        logs = [{"timestamp": 123541423, "message": "TestLog"}]
        self.z.sendLog('ZeusTest', logs)
        mock_requests.post.assert_called_with(FAKE_SERVER + '/logs/' +
                                              FAKE_TOKEN + '/ZeusTest/',
                                              data={"logs": json.dumps(logs)})

    @mock.patch('zeus.client.requests')
    def test_post_single_log_wrong_name(self, mock_requests):
        logs = [{"message": "TestLog", "value": 23}]
        self.assertRaises(
            client.ZeusException, self.z.sendLog, 'W.rongName', logs)
        self.assertRaises(
            client.ZeusException, self.z.sendLog, '_WrongName', logs)
        self.assertRaises(
            client.ZeusException, self.z.sendLog, 'W#?rongName', logs)
        self.assertRaises(
            client.ZeusException, self.z.sendLog, 'W-rongName', logs)

    @mock.patch('zeus.client.requests')
    def test_post_multiple_logs(self, mock_requests):
        logs = [{"timestamp": 123541423, "message": "TestLog"},
                {"timestamp": 123541424, "message": "TestLog2"},
                {"timestamp": 123541425, "message": "TestLog3"}, ]
        self.z.sendLog('ZeusTest', logs)
        mock_requests.post.assert_called_with(FAKE_SERVER + '/logs/' +
                                              FAKE_TOKEN + '/ZeusTest/',
                                              data={"logs": json.dumps(logs)})

    @mock.patch('zeus.client.requests')
    def test_get_logs(self, mock_requests):
        self.z.getLog('ZeusTest',
                      pattern='*',
                      from_date=123456789,
                      to_date=126235344235,
                      offset=23,
                      limit=10)
        mock_requests.get.assert_called_with(FAKE_SERVER + '/logs/' +
                                             FAKE_TOKEN + '/',
                                             params={'log_name': 'ZeusTest',
                                                     'pattern': '*',
                                                     'from': 123456789,
                                                     'to': 126235344235,
                                                     'offset': 23,
                                                     'limit': 10})

    @mock.patch('zeus.client.requests')
    def test_post_empty_metric(self, mock_requests):
        metrics = []
        self.z.sendMetric('ZeusTest', metrics)
        mock_requests.post.assert_called_with(FAKE_SERVER + '/metrics/' +
                                              FAKE_TOKEN + '/ZeusTest/',
                                              data={"metrics":
                                                    json.dumps(metrics)})

    @mock.patch('zeus.client.requests')
    def test_post_single_metric(self, mock_requests):
        metrics = [{"timestamp": 123541423, "value": 0}]
        self.z.sendMetric('Zeus.Test', metrics)
        mock_requests.post.assert_called_with(FAKE_SERVER + '/metrics/' +
                                              FAKE_TOKEN + '/Zeus.Test/',
                                              data={"metrics":
                                                    json.dumps(metrics)})

    @mock.patch('zeus.client.requests')
    def test_post_single_metric_wrong_name(self, mock_requests):
        metrics = [{"timestamp": 123541423, "value": 0}]
        self.assertRaises(
            client.ZeusException, self.z.sendMetric, '_WrongName', metrics)
        self.assertRaises(
            client.ZeusException, self.z.sendMetric, 'W#?rongName', metrics)

    @mock.patch('zeus.client.requests')
    def test_post_multiple_metrics(self, mock_requests):
        metrics = [{"timestamp": 123541423, "value": 0},
                   {"timestamp": 123541424, "value": 1},
                   {"timestamp": 123541425, "value": 2.0}, ]
        self.z.sendMetric('ZeusTest', metrics)
        mock_requests.post.assert_called_with(FAKE_SERVER + '/metrics/' +
                                              FAKE_TOKEN + '/ZeusTest/',
                                              data={"metrics":
                                                    json.dumps(metrics)})

    @mock.patch('zeus.client.requests')
    def test_get_metric_values(self, mock_requests):
        self.z.getMetric(metric_name='ZeusTest',
                         aggregator='sum',
                         from_date=123456789,
                         to_date=126235344235,
                         group_interval='1m',
                         filter_condition='value > 90',
                         limit=10)
        mock_requests.get.assert_called_with(FAKE_SERVER + '/metrics/' +
                                             FAKE_TOKEN + '/_values/',
                                             params={'metric_name': 'ZeusTest',
                                                     'aggregator_function':
                                                     'sum',
                                                     'from': 123456789,
                                                     'to': 126235344235,
                                                     'group_interval': '1m',
                                                     'filter_condition':
                                                     'value > 90',
                                                     'limit': 10})

    @mock.patch('zeus.client.requests')
    def test_get_metric_names(self, mock_requests):
        self.z.getMetricNames(metric_name='ZeusTest',
                              limit=10)
        mock_requests.get.assert_called_with(FAKE_SERVER + '/metrics/' +
                                             FAKE_TOKEN + '/_names/',
                                             params={'metric_name': 'ZeusTest',
                                                     'limit': 10})

    @mock.patch('zeus.client.requests')
    def tearDown(self, mock_requests):
        pass

if __name__ == '__main__':
    unittest.main()
