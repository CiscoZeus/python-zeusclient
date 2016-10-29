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
from utils import validateLogName, validateDates


class LogsInterface(object):

    def __init__(self, user_token, rest_client):
        self.token = user_token
        self.rest_client = rest_client

    def sendLog(self, log_name, logs):
        """Return ``dict`` saying how many *logs* were successfully inserted
        with *log_name*.

        :param string log_name: String with the name of the log.
        :param dict logs: ``array`` of ``dict`` containing the logs to send.
        :rtype: dict

        """
        validateLogName(log_name)
        data = {'logs': json.dumps(logs)}
        return self.rest_client.sendPostRequest('/logs/' + self.token +
                                                '/' + log_name + '/', data)

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
        validateDates(from_date, to_date)
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

        return self.rest_client.sendGetRequest('/logs/' + self.token + '/',
                                               data)
