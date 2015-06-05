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
import re


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
        elif method == 'DELETE':
            r = requests.delete(self.server + path)

        return r.status_code, r.json()

    def _validateLogName(self, name):
        if name is None:
            raise ZeusException("Invalid input. Log name cannot be None.")
        name_length = len(name)
        if name_length < 1 or name_length > 255:
            raise ZeusException("Invalid log name. It must be longer than 1 "
                                "character and shorter than 255 charaters.")
        if not re.match(r"^[a-zA-Z0-9]*$", name):
            raise ZeusException("Invalid log name. It can only contain "
                                "letters or numbers.")

    def _validateMetricName(self, name):
        if name is None:
            raise ZeusException("Invalid input. Metric name cannot be None.")
        name_length = len(name)
        if name_length < 1 or name_length > 255:
            raise ZeusException("Invalid metric name. It must be longer than "
                                "1 character and shorter than 255 charaters.")
        if not re.match(r"^[^_.-][.\w-]*$", name):
            raise ZeusException("Invalid metric name. The name needs to start "
                                "with a letter or number and can contain "
                                "_ - or .")

    def _validateDates(self, from_date, to_date):
        try:
            from_date_value = float(from_date) if from_date else None
            to_date_value = float(to_date) if to_date else None
        except ValueError as e:
            raise ZeusException("Invalid date. %s" % str(e))
        if (from_date_value is None) or (to_date_value is None):
            return
        elif from_date_value > to_date_value:
            raise ZeusException("Invalid date. The from_date should not be "
                                "after to_date.")

    def sendLog(self, log_name, logs):
        """Return ``dict`` saying how many *logs* were successfully inserted
        with *log_name*.

        :param string log_name: String with the name of the log.
        :param dict logs: ``array`` of ``dict`` containing the logs to send.
        :rtype: dict

        """
        self._validateLogName(log_name)
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
        self._validateMetricName(metric_name)
        data = {'metrics': json.dumps(metrics)}
        return self._sendRequest('POST', '/metrics/' + self.token +
                                 '/' + metric_name + '/', data)

    def getLog(self,
               log_name,
               attribute_name=None,
               pattern=None,
               from_date=None,
               to_date=None,
               offset=None,
               limit=None):
        """Return ``array`` of ``dict`` with the logs that match the params.

        :param string log_name: Name of the log.
        :param string attribute_name: Name of field to be searched. If omitted,
        search all fields.
        :param string pattern: Pattern to match the logs against.
        :param string from_date: Unix formatted start date.
        :param string to_date: Unix formatted end date.
        :param string offset: Result offset.
        :param string limit: Max number of results in the return.
        :rtype: array

        """
        self._validateDates(from_date, to_date)
        data = {"log_name": log_name}
        if attribute_name:
            data['attribute_name'] = attribute_name
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

    def getMetric(self, metric_name,
                  from_date=None,
                  to_date=None,
                  aggregator_function=None,
                  aggregator_column=None,
                  group_interval=None,
                  filter_condition=None,
                  offset=None,
                  limit=None):
        """Return ``array`` of ``dict`` with the metrics that match the params.

        :param string metric_name: Name of the metric.
        :param string from_date: Unix formatted start date.
        :param string to_date: Unix formatted end date.
        :param string aggregator_function: Aggregator function. ``sum``,
        ``count``, ``min``, ``max``,...
        :param string aggregator_column: Column to which
        ``aggregator_function`` is to be applied.
        :param string group_interval: Intervals in which to group the results.
        :param string filter_condition: Filters to be applied to metric values.
        :param string offset: Result offset.
        :param string limit: Max number of results in the return.
        :rtype: array

        """
        self._validateDates(from_date, to_date)
        data = {"metric_name": metric_name}
        if from_date:
            data['from'] = from_date
        if to_date:
            data['to'] = to_date
        if aggregator_function:
            # EG. 'sum'
            data['aggregator_function'] = aggregator_function
        if aggregator_column:
            # EG. 'sum'
            data['aggregator_column'] = aggregator_column
        if group_interval:
            # EG. '1m'
            data['group_interval'] = group_interval
        if filter_condition:
            # EG. '"Values" < 33'
            data['filter_condition'] = filter_condition
        if limit:
            data['limit'] = limit
        if offset:
            data['offset'] = offset

        return self._sendRequest('GET', '/metrics/' + self.token +
                                 '/_values/', data)

    def getMetricNames(self, metric_name=None, limit=None, offset=None):
        """Return ``array`` of ``string`` with the metric names that match the
        params.

        :param string metric_name: Pattern for the metric name.
        :param string limit: Max number of results in the return.
        :param string limit: Starting offset in the resulting list. The default
        value is 0 (first result).
        :rtype: array

        """
        data = {}
        if metric_name:
            data['metric_name'] = metric_name
        if limit:
            data['limit'] = limit
        if offset:
            data['offset'] = offset

        return self._sendRequest('GET', '/metrics/' + self.token +
                                 '/_names/', data)

    def deleteMetric(self, metric_name):
        """Delete an entire metric from Zeus.

        :param string metric_name: Pattern for the metric name.
        :rtype: boolean

        """
        self._validateMetricName(metric_name)
        return self._sendRequest('DELETE', '/metrics/' + self.token +
                                 '/' + metric_name + '/', None)


class ZeusException(Exception):
    pass


# class Log():

#     def __init__(self, name, data, timestamp=None):
#         self.name = name
#         self.timestamp = timestamp
#         self.data = data

#     def package(self):
#         l = {}
