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

import requests
from urlparse import urlparse
from urlparse import urljoin

METHOD_POST = 'POST'
METHOD_GET = 'GET'
METHOD_PUT = 'PUT'
METHOD_DELETE = 'DELETE'


class RestClient(object):

    def __init__(self, server):
        # makes sure we always use https
        url_object = urlparse(server)
        url_parts = list(url_object)
        url_parts[0] = "https://"
        self.server = ''.join(url_parts)

    def _sendRequest(self, method, path, data=None, headers=None):
        final_url = urljoin(self.server, path)
        if method == METHOD_POST:
            r = requests.post(final_url, data=data, headers=headers)
        elif method == METHOD_GET:
            r = requests.get(final_url, params=data)
        elif method == METHOD_DELETE:
            r = requests.delete(final_url)
        elif method == METHOD_PUT:
            r = requests.put(final_url, data=data, headers=headers)

        if r.status_code == 500:
            raise Exception("Internal Server Error")
        try:
            return r.status_code, r.json()
        except Exception:
            return r.status_code

    def sendPostRequest(self, path, data=None, headers=None):
        return self._sendRequest(METHOD_POST, path, data, headers)

    def sendGetRequest(self, path, data=None, headers=None):
        return self._sendRequest(METHOD_GET, path, data, headers)

    def sendPutRequest(self, path, data=None, headers=None):
        return self._sendRequest(METHOD_PUT, path, data, headers)

    def sendDeleteRequest(self, path, data=None, headers=None):
        return self._sendRequest(METHOD_DELETE, path, data, headers)
