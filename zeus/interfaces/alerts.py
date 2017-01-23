# -*- coding: utf-8 -*-

# Copyright 2016 Cisco Systems, Inc.
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

import json


class AlertsInterface(object):

    def __init__(self, user_token, rest_client):
        self.token = user_token
        self.rest_client = rest_client

    def createAlert(
            self, alert_name, username, alerts_type, alert_expression,
            alert_severity, metric_name, emails, status, notify_period
    ):

        """Creates a new alert, returns status code of creation
        and alert parameters

        :param alert_name: Name of the alert
        :param username: User the alert belongs to
        :param alerts_type: "metric" or "log"
        :param alert_expression: expression to evaluate the alert
        (eg. "cpu.value > 20")
        :param alert_severity: severity level of the alert
        :param metric_name: metric associated with the alert
        :param emails: emails to receive notification when the alert triggers
        :param status: if the alert is active or disable
        :param notify_period: frequency of notifications

        :rtype: array
        """

        data = {
            'alert_name': alert_name,
            'username': username,
            'token': self.token,
            'alerts_type': alerts_type,
            'alert_expression': alert_expression,
            'alert_severity': alert_severity,
            'metric_name': metric_name,
            'emails': emails,
            'status': status,
            'notify_period': notify_period
        }
        path = '/alerts/' + self.token
        header = {'content-type': 'application/json'}

        return self.rest_client.sendPostRequest(path, json.dumps(data), header)

    def getAlerts(self):

        """Return all alerts

        :rtype: array
        """
        path = '/alerts/' + self.token
        return self.rest_client.sendGetRequest(path)

    def modifyAlert(
            self, alert_id, alert_name, username, alerts_type,
            alert_expression, alert_severity, metric_name, emails, status,
            notify_period
    ):

        """Modifies an existing alert with new data

        :param alert_id: Id of the alert to be modified
        :param alert_name: Name of the alert
        :param username: User the alert belongs to
        :param alerts_type: "metric" or "log"
        :param alert_expression: expression to evaluate the alert
        (eg. "cpu.value > 20")
        :param alert_severity: severity level of the alert
        :param metric_name: metric associated with the alert
        :param emails: emails to receive notification when the alert triggers
        :param status: if the alert is active or disable
        :param notify_period: frequency of notifications

        :rtype: array
        """

        data = {
            'alert_name': alert_name,
            'username': username,
            'token': self.token,
            'alerts_type': alerts_type,
            'alert_expression': alert_expression,
            'alert_severity': alert_severity,
            'metric_name': metric_name,
            'emails': emails,
            'status': status,
            'notify_period': notify_period
        }
        path = '/alerts/' + self.token + '/' + str(alert_id)
        header = {'content-type': 'application/json'}

        return self.rest_client.sendPutRequest(path, json.dumps(data), header)

    def getAlert(self, alert_id):

        """Return an specific alert information

        :param alert_id: Id of the alert to be returned

        :rtype: array
        """
        path = '/alerts/' + self.token + '/' + str(alert_id)
        return self.rest_client.sendGetRequest(path)

    def deleteAlert(self, alert_id):
        """Delete an specific alert

        :param alert_id: Id of the alert to be deleted

        :rtype: array
        """
        path = '/alerts/' + self.token + '/' + str(alert_id)
        return self.rest_client.sendDeleteRequest(path)

    def enableAlerts(self, alert_id_list):

        """Bulk enable alerts

        :param alert_id_list: List of ids of the alerts to be enabled

        :rtype: array
        """
        data = {
            'id': alert_id_list
        }
        path = '/alerts/' + self.token + '/enable'
        header = {'content-type': 'application/json'}

        return self.rest_client.sendPostRequest(path, json.dumps(data), header)

    def disableAlerts(self, alert_id_list):

        """Bulk disable alerts

        :param alert_id_list: List of ids of the alerts to be disabled

        :rtype: array
        """

        data = {
            'id': alert_id_list
        }
        path = '/alerts/' + self.token + '/disable'
        header = {'content-type': 'application/json'}

        return self.rest_client.sendPostRequest(path, json.dumps(data), header)
