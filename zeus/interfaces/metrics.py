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
from utils import validate_metric_name, validate_dates


def send_metric(cls, metric_name, metrics):
    """Return ``dict`` saying how many *metrics* were successfully inserted
    with *metric_name*.

    :param cls: class object
    :type cls: ZeusClient
    :param string metric_name: String with the name of the metric.
    :param dict metrics: ``array`` of ``dict`` containing the metrics to
     send.
    :rtype: dict
    """

    path = '/metrics/{}/{}'.format(cls.token, metric_name)
    validate_metric_name(metric_name)
    data = {'metrics': json.dumps(metrics)}

    return cls._request('POST', path=path, data=data)


def get_metric(cls, metric_name,
               from_date=None,
               to_date=None,
               aggregator_function=None,
               aggregator_column=None,
               group_interval=None,
               filter_condition=None,
               offset=None,
               limit=None):
    """Return ``array`` of ``dict`` with the metrics that match the params.

    :param cls: class object
    :type cls: ZeusClient
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

    path = '/metrics/{}/_values'.format(cls.token)
    validate_dates(from_date, to_date)
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

    return cls._request('GET', path=path, data=data)


def get_metric_names(cls, metric_name=None, limit=None, offset=None):
    """Return ``array`` of ``string`` with the metric names that match the
    params.

    :param cls: class object
    :type cls: ZeusClient
    :param string metric_name: Pattern for the metric name.
    :param string limit: Max number of results in the return.
    :param string limit: Starting offset in the resulting list. The default
    value is 0 (first result).
    :rtype: array
    """

    path = '/metrics/{}/_names'.format(cls.token)
    data = {}
    if metric_name:
        data['metric_name'] = metric_name
    if limit:
        data['limit'] = limit
    if offset:
        data['offset'] = offset

    return cls._request('GET', path=path, data=data)


def delete_metric(cls, metric_name):
    """Delete an entire metric from Zeus.

    :param cls: class object
    :type cls: ZeusClient
    :param string metric_name: Pattern for the metric name.
    :rtype: boolean
    """

    path = '/metrics/{}/{}'.format(cls.token, metric_name)
    validate_metric_name(metric_name)

    return cls._request('DELETE', path=path)
