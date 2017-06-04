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

import requests
import urlparse

from interfaces.logs import get_log
from interfaces.logs import send_log
from interfaces.metrics import send_metric
from interfaces.metrics import delete_metric
from interfaces.metrics import get_metric
from interfaces.metrics import get_metric_names
from interfaces.alerts import create_alert
from interfaces.alerts import delete_alert
from interfaces.alerts import disable_alerts
from interfaces.alerts import enable_alerts
from interfaces.alerts import get_alert
from interfaces.alerts import get_alerts
from interfaces.alerts import modify_alert
from interfaces.trigalerts import get_triggered_alerts
from interfaces.trigalerts import get_triggered_alerts_last24_hours


class ZeusClient(object):
    """
    Zeus Client class, implementing wrapper methods for the Zeus API.
    """

    def __init__(self, token, endpoint='https://api.ciscozeus.io'):
        """
        :param token: either user token or external token.
        :type token: str
        :param endpoint: URL endpoints
        :type endpoint: str
        """
        self.token = token

        # TODO 1. Better to separate into function and add test code against it.
        url_object = urlparse.urlparse(endpoint)
        url_parts = list(url_object)
        url_parts[0] = "https://"
        self.endpoint = ''.join(url_parts)

        self.headers = {
            'Authorization': "Bearer {}".format(self.token),
            'content-type': 'application/json'
        }

        self.bucket_name = None
        self.timeout_sec = 20

    def bucket(self, bucket_name):
        """
        This method is for method chain purpose.

        :param bucket_name: target bucket name
        :type bucket_name: str
        :return: self object.
        :rtype: ZeusClient
        """
        self.bucket_name = bucket_name
        return self

    def __build_header(self):
        """
        Make HTTP Header
        :return: Header Object
        :rtype: dict
        """
        if self.bucket_name is None:
            return self.headers

        return dict(self.headers, **{'Bucket-Name': self.bucket_name})

    def _request(self, method, path, data=None):
        """
        :param method: HTTTP Method ['GET', 'POST', 'PUT'. 'DELETE']
        :type method: str
        :param path: url path start with '/'
        :type path: str
        :param data: data to be sent
        :type data: dict
        :param headers: HTTP Header
        :type headers: dict
        """
        url = urlparse.urljoin(self.endpoint, path)

        if method.upper() == 'GET':
            response = requests.get(
                url, params=data, headers=self.__build_header(),
                timeout=self.timeout_sec
            )

        elif method.upper() == 'POST':
            response = requests.post(
                url, data=data, headers=self.__build_header(),
                timeout=self.timeout_sec
            )

        elif method.upper() == 'PUT':
            response = requests.put(
                url, data=data, headers=self.__build_header(),
                timeout=self.timeout_sec
            )

        elif method.upper() == 'DELETE':
            response = requests.delete(
                url, headers=self.__build_header(),
                timeout=self.timeout_sec
            )

        else:  # TODO Define exception more properly
            raise Exception('Unknown method {}'.format(method))

        # TODO better to make a function to clean method chain related variables.
        if self.bucket_name is not None:
            self.bucket_name = None

        return response


# Logs
ZeusClient.getLog = get_log
ZeusClient.sendLog = send_log

# Metrics
ZeusClient.sendMetric = send_metric
ZeusClient.deleteMetric = delete_metric
ZeusClient.getMetric = get_metric
ZeusClient.getMetricNames = get_metric_names

# Alerts
ZeusClient.createAlert = create_alert
ZeusClient.deleteAlert = delete_alert
ZeusClient.disableAlerts = disable_alerts
ZeusClient.enableAlerts = enable_alerts
ZeusClient.getAlert = get_alert
ZeusClient.getAlerts = get_alerts
ZeusClient.modifyAlert = modify_alert

# Trigger Alerts
ZeusClient.getTriggeredAlerts = get_triggered_alerts
ZeusClient.getTriggeredAlertsLast24Hours = get_triggered_alerts_last24_hours
