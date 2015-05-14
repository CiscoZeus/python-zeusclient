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

import json
import requests


class ZeusClient():

    """Zeus Client class, implementing wrapper methods for the
    Zeus API.

    """

    def __init__(self, user_token, server):
        self.token = user_token
        if not server.startswith('http://'):
            self.server = 'http://' + server
        else:
            self.server = server

    def _sendRequest(self, method, path, data):
        if method == 'POST':
            r = requests.post(self.server + path, data=data)
        elif method == 'GET':
            r = requests.get(self.server + path, params=data)

        return r.status_code, r.json()

    def sendLog(self, log_name, logs):
        """Return ``dict`` saying how many *logs* were successfully inserted
        with *log_name*.

        :param string log_name: String with the name of the log.
        :param dict logs: ``array`` of ``dict`` containing the logs to send.
        :rtype: dict

        """
        data = {'logs': json.dumps(logs)}
        return self._sendRequest('POST', '/logs/' + self.token +
                                 '/' + log_name + '/', data)

    def sendMetric(self, metric_name, metrics):
        """Return ``dict`` saying how many *metrics* were successfully inserted
        with *metric_name*.

        :param string metric_name: String with the name of the metric.
        :param dict metrics: ``array`` of ``dict`` containing the metrics to
         send.
        :rtype: dict

        """
        data = {'metrics': json.dumps(metrics)}
        return self._sendRequest('POST', '/metrics/' + self.token +
                                 '/' + metric_name + '/', data)

    def getLog(self,
               log_name,
               pattern=None,
               from_date=None,
               to_date=None,
               offset=None,
               limit=None):
        """Return ``array`` of ``dict`` with the logs that match the params.

        :param string log_name: Name of the log.
        :param string pattern: Pattern to match the logs against.
        :param string from_date: Unix formatted start date.
        :param string to_date: Unix formatted end date.
        :param string offset: Result offset.
        :param string limit: Max number of results in the return.
        :rtype: array

        """
        data = {"log_name": log_name}
        if pattern:
            data['pattern'] = pattern
        if from_date:
            data['from'] = from_date
        if to_date:
            data['to'] = to_date
        if offset:
            data['offset'] = offset
        if limit:
            data['limit'] = limit

        return self._sendRequest('GET', '/logs/' + self.token + '/', data)

    def getMetric(self, metric_name=None,
                  from_date=None,
                  to_date=None,
                  aggregator=None,
                  group_interval=None,
                  filter_condition=None,
                  limit=None):
        """Return ``array`` of ``dict`` with the metrics that match the params.

        :param string metric_name: Name of the metric.
        :param string from_date: Unix formatted start date.
        :param string to_date: Unix formatted end date.
        :param string aggregator: Aggregator function. ``sum``, ``count``,
        ``min``, ``max``,...
        :param string group_interval: Intervals in which to group the results.
        :param string offset: Result offset.
        :param string limit: Max number of results in the return.
        :rtype: array

        """
        data = {}
        if metric_name:
            data['metric_name'] = metric_name
        if from_date:
            data['from'] = from_date
        if to_date:
            data['to'] = to_date
        if aggregator:
            # EG. 'sum'
            data['aggregator_function'] = aggregator
        if group_interval:
            # EG. '1m'
            data['group_interval'] = group_interval
        if filter_condition:
            # EG. '"Values" < 33'
            data['filter_condition'] = filter_condition
        if limit:
            data['limit'] = limit

        return self._sendRequest('GET', '/metrics/' + self.token +
                                 '/_values/', data)

    def getMetricNames(self, metric_name=None, limit=None):
        """Return ``array`` of ``string`` with the metric names that match the
        params.

        :param string metric_name: Pattern for the metric name.
        :param string limit: Max number of results in the return.
        :rtype: array

        """
        data = {}
        if metric_name:
            data['metric_name'] = metric_name
        if limit:
            data['limit'] = limit

        return self._sendRequest('GET', '/metrics/' + self.token +
                                 '/_names/', data)
