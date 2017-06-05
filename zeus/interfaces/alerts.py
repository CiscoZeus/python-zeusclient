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


def create_alert(
    cls, alert_name, username, alerts_type, alert_expression,
    alert_severity, metric_name, emails, status, notify_period
):
    """Creates a new alert, returns status code of creation
    and alert parameters

    :param cls: class object
    :type cls: ZeusClient
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
        'token': cls.token,
        'alerts_type': alerts_type,
        'alert_expression': alert_expression,
        'alert_severity': alert_severity,
        'metric_name': metric_name,
        'emails': emails,
        'status': status,
        'notify_period': notify_period
    }
    path = '/alerts/{}'.format(cls.token)

    return cls._request('POST', path=path, data=json.dumps(data))


def get_alerts(cls):
    """Return all alerts

    :param cls: class object
    :type cls: ZeusClient

    :rtype: array
    """
    path = '/alerts/{}'.format(cls.token)
    return cls._request('GET', path=path)


def modify_alert(
    cls, alert_id, alert_name, username, alerts_type,
    alert_expression, alert_severity, metric_name, emails, status,
    notify_period
):
    """Modifies an existing alert with new data

    :param cls: class object
    :type cls: ZeusClient
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
        'token': cls.token,
        'alerts_type': alerts_type,
        'alert_expression': alert_expression,
        'alert_severity': alert_severity,
        'metric_name': metric_name,
        'emails': emails,
        'status': status,
        'notify_period': notify_period
    }
    path = '/alerts/{}/{}'.format(cls.token, str(alert_id))

    return cls._request('PUT', path=path, data=json.dumps(data))


def get_alert(cls, alert_id):
    """Return an specific alert information

    :param cls: class object
    :type cls: ZeusClient
    :param alert_id: Id of the alert to be returned

    :rtype: array
    """
    path = '/alerts/{}/{}'.format(cls.token, str(alert_id))

    return cls._request('GET', path=path)


def delete_alert(cls, alert_id):
    """Delete an specific alert

    :param cls: class object
    :type cls: ZeusClient
    :param alert_id: Id of the alert to be deleted

    :rtype: array
    """
    path = '/alerts/{}/{}'.format(cls.token, str(alert_id))
    return cls._request('DELETE', path=path)


def enable_alerts(cls, alert_id_list):
    """Bulk enable alerts

    :param cls: class object
    :type cls: ZeusClient
    :param alert_id_list: List of ids of the alerts to be enabled

    :rtype: array
    """
    path = '/alerts/{}/enable'.format(cls.token)
    data = {'id': alert_id_list}

    return cls._request('POST', path=path, data=json.dumps(data))


def disable_alerts(cls, alert_id_list):
    """Bulk disable alerts

    :param cls: class object
    :type cls: ZeusClient
    :param alert_id_list: List of ids of the alerts to be disabled

    :rtype: array
    """
    path = '/alerts/{}/disable'.format(cls.token)
    data = {'id': alert_id_list}

    return cls._request('POST', path=path, data=json.dumps(data))
