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


def get_triggered_alerts(cls):
    """Return all triggered alerts

    :param cls: class object
    :type cls: ZeusClient
    :rtype: array
    """
    path = '/triggeredalerts/{}'.format(cls.token)

    return cls._request('GET', path=path)


def get_triggered_alerts_last24_hours(cls):
    """Return all triggered alerts in the last 24 hours

    :param cls: class object
    :type cls: ZeusClient
    :rtype: array
    """
    path = '/triggeredalerts/{}/last24'.format(cls.token)

    return cls._request('GET', path=path)
