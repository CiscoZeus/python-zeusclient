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
import posixpath
import unittest
import urlparse

from zeus import client
from zeus.interfaces.utils import validateDates, ZeusException

FAKE_TOKEN = 'ZeUsRoCkS'
FAKE_SERVER = 'https://zeus.rocks'


class TestZeusClient(unittest.TestCase):
    def setUp(self):
        # Setting up a Zeus client with a fake token:
        self.z = client.ZeusClient(FAKE_TOKEN, FAKE_SERVER)
        self.fake_headers = {
            'Authorization': "Bearer {}".format(FAKE_TOKEN),
            'content-type': 'application/json'
        }

    def fake_header_with_z_resource(self, bucket_name):
        """
        Make HTTP Header
        :param bucket_name: bucket name
        :type bucket_name: str
        :return: Header Object
        :rtype: dict
        """
        return dict(self.fake_headers, **{'Bucket-Name': bucket_name})

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
        url = urlparse.urljoin(FAKE_SERVER,
                               posixpath.join('logs', FAKE_TOKEN, 'ZeusTest'))
        self.z.sendLog('ZeusTest', logs)
        mock_requests.post.assert_called_with(
            url, data={"logs": json.dumps(logs)},
            headers=self.fake_header_with_z_resource('ZeusTest'), timeout=20)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_post_single_log(self, mock_requests):
        url = urlparse.urljoin(
            FAKE_SERVER, posixpath.join('logs', FAKE_TOKEN, 'ZeusTest'))
        logs = [{"timestamp": 123541423, "key": "TestLog", "key2": 123}]
        self.z.sendLog('ZeusTest', logs)
        mock_requests.post.assert_called_with(
            url, data={"logs": json.dumps(logs)},
            headers=self.fake_header_with_z_resource('ZeusTest'), timeout=20)

    def test_post_single_log_wrong_name(self):
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
        url = urlparse.urljoin(
            FAKE_SERVER, posixpath.join('logs', FAKE_TOKEN, 'ZeusTest'))
        logs = [{"timestamp": 123541423, "message": "TestLog"},
                {"timestamp": 123541424, "message": "TestLog2"},
                {"timestamp": 123541425, "message": "TestLog3"}, ]
        self.z.sendLog('ZeusTest', logs)
        mock_requests.post.assert_called_with(
            url, data={"logs": json.dumps(logs)},
            headers=self.fake_header_with_z_resource('ZeusTest'), timeout=20)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_get_logs(self, mock_requests):
        url = urlparse.urljoin(FAKE_SERVER, posixpath.join('logs', FAKE_TOKEN))
        self.z.getLog('ZeusTest',
                      attribute_name='message',
                      pattern='*',
                      from_date=123456789,
                      to_date=126235344235,
                      offset=23,
                      limit=10)
        mock_requests.get.assert_called_with(
            url,
            params={
                'log_name': 'ZeusTest',
                'attribute_name': 'message',
                'pattern': '*',
                'from': 123456789,
                'to': 126235344235,
                'offset': 23,
                'limit': 10},
            timeout=20)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_post_empty_metric(self, mock_requests):
        url = urlparse.urljoin(
            FAKE_SERVER, posixpath.join('metrics', FAKE_TOKEN, 'ZeusTest'))
        metrics = []
        self.z.sendMetric('ZeusTest', metrics)
        mock_requests.post.assert_called_with(
            url, data={"metrics": json.dumps(metrics)},
            headers=self.fake_header_with_z_resource('ZeusTest'), timeout=20)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_post_single_metric(self, mock_requests):
        url = urlparse.urljoin(
            FAKE_SERVER, posixpath.join('metrics', FAKE_TOKEN, 'Zeus.Test'))
        metrics = [{"timestamp": 123541423, "value": 0}]
        self.z.sendMetric('Zeus.Test', metrics)
        mock_requests.post.assert_called_with(
            url, data={"metrics": json.dumps(metrics)},
            headers=self.fake_header_with_z_resource('Zeus.Test'),
            timeout=20)

    def test_post_single_metric_wrong_name(self):
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
        url = urlparse.urljoin(
            FAKE_SERVER, posixpath.join('metrics', FAKE_TOKEN, 'ZeusTest'))
        metrics = [{"timestamp": 123541423, "value": 0},
                   {"timestamp": 123541424, "value": 1},
                   {"timestamp": 123541425, "value": 2.0}, ]
        self.z.sendMetric('ZeusTest', metrics)
        mock_requests.post.assert_called_with(
            url, data={"metrics": json.dumps(metrics)},
            headers=self.fake_header_with_z_resource('ZeusTest'), timeout=20)

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
        mock_requests.get.assert_called_with(
            FAKE_SERVER + '/metrics/' +
            FAKE_TOKEN + '/_values',
            params={
                'metric_name': 'ZeusTest',
                'aggregator_function': 'sum',
                'aggregator_column': 'val1',
                'from': 123456789,
                'to': 126235344235,
                'group_interval': '1m',
                'filter_condition': 'value > 90',
                'limit': 10,
                'offset': 20}, timeout=20)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_get_metric_names(self, mock_requests):
        self.z.getMetricNames(metric_name='ZeusTest',
                              limit=10,
                              offset=20)
        mock_requests.get.assert_called_with(FAKE_SERVER + '/metrics/' +
                                             FAKE_TOKEN + '/_names',
                                             params={'metric_name': 'ZeusTest',
                                                     'limit': 10,
                                                     'offset': 20}, timeout=20)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_get_delete_metric(self, mock_requests):
        self.z.deleteMetric('ZeusTest')
        mock_requests.delete.assert_called_with(
            FAKE_SERVER + '/metrics/' +
            FAKE_TOKEN + '/ZeusTest',
            timeout=20
        )

    @mock.patch('zeus.interfaces.rest.requests')
    def test_create_alert(self, mock_requests):
        alert_name = "testerino"
        username = "pelegrino"
        token = FAKE_TOKEN
        alerts_type = "metric"
        alert_expression = "cpu.value > 20"
        alert_severity = "S1"
        metric_name = "cpu.value"
        emails = "john1234@gmail.com"
        status = "active"
        notify_period = 60

        self.z.createAlert(alert_name, username, alerts_type,
                           alert_expression, alert_severity, metric_name,
                           emails, status, notify_period)
        data = {
            'alert_name': alert_name,
            'username': username,
            'token': token,
            'alerts_type': alerts_type,
            'alert_expression': alert_expression,
            'alert_severity': alert_severity,
            'metric_name': metric_name,
            'emails': emails,
            'status': status,
            'notify_period': notify_period
        }

        mock_requests.post.assert_called_with(
            FAKE_SERVER + '/alerts/' +
            FAKE_TOKEN, data=json.dumps(data),
            headers=self.fake_headers, timeout=20)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_modify_alert(self, mock_requests):
        alert_id = 42
        alert_name = "testerino"
        username = "pelegrino"
        token = FAKE_TOKEN
        alerts_type = "metric"
        alert_expression = "cpu.value > 20"
        alert_severity = "S1"
        metric_name = "cpu.value"
        emails = "john1234@gmail.com"
        status = "active"
        notify_period = 60

        self.z.modifyAlert(alert_id, alert_name, username, alerts_type,
                           alert_expression, alert_severity, metric_name,
                           emails, status, notify_period)
        data = {
            'alert_name': alert_name,
            'username': username,
            'token': token,
            'alerts_type': alerts_type,
            'alert_expression': alert_expression,
            'alert_severity': alert_severity,
            'metric_name': metric_name,
            'emails': emails,
            'status': status,
            'notify_period': notify_period
        }

        path = FAKE_SERVER + '/alerts/' + FAKE_TOKEN + '/' + str(alert_id)
        mock_requests.put.assert_called_with(
            path, data=json.dumps(data),
            headers=self.fake_headers, timeout=20)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_get_alerts(self, mock_requests):
        self.z.getAlerts()

        path = FAKE_SERVER + '/alerts/' + FAKE_TOKEN
        mock_requests.get.assert_called_with(path, params=None, timeout=20)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_get_alert(self, mock_requests):
        alert_id = 42
        self.z.getAlert(alert_id)

        path = FAKE_SERVER + '/alerts/' + FAKE_TOKEN + '/' + str(alert_id)
        mock_requests.get.assert_called_with(path, params=None, timeout=20)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_delete_alert(self, mock_requests):
        alert_id = 42
        self.z.deleteAlert(alert_id)

        path = FAKE_SERVER + '/alerts/' + FAKE_TOKEN + '/' + str(alert_id)
        mock_requests.delete.assert_called_with(path, timeout=20)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_enable_alerts(self, mock_requests):
        alert_id_list = [19, 42]
        self.z.enableAlerts(alert_id_list)
        data = {
            'id': alert_id_list
        }

        path = FAKE_SERVER + '/alerts/' + FAKE_TOKEN + '/enable'
        mock_requests.post.assert_called_with(
            path, data=json.dumps(data),
            headers=self.fake_headers, timeout=20)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_disable_alerts(self, mock_requests):
        alert_id_list = [19, 42]
        self.z.disableAlerts(alert_id_list)
        data = {
            'id': alert_id_list
        }

        path = FAKE_SERVER + '/alerts/' + FAKE_TOKEN + '/disable'
        mock_requests.post.assert_called_with(
            path, data=json.dumps(data),
            headers=self.fake_headers, timeout=20)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_get_triggered_alerts(self, mock_requests):
        self.z.getTriggeredAlerts()

        path = FAKE_SERVER + '/triggeredalerts/' + FAKE_TOKEN
        mock_requests.get.assert_called_with(path, params=None, timeout=20)

    @mock.patch('zeus.interfaces.rest.requests')
    def test_get_triggered_alerts_last_24h(self, mock_requests):
        self.z.getTriggeredAlertsLast24Hours()

        path = FAKE_SERVER + '/triggeredalerts/' + FAKE_TOKEN + "/last24"
        mock_requests.get.assert_called_with(path, params=None, timeout=20)

    def test_get_delete_metric_wrong_name(self):
        self.assertRaises(ZeusException, self.z.deleteMetric, '_WrongName')

    @mock.patch('zeus.interfaces.rest.requests')
    def tearDown(self, mock_requests):
        pass


if __name__ == '__main__':
    unittest.main()
