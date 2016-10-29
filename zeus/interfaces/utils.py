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

import re


def validateMetricName(name):
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


def validateDates(from_date, to_date):
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


def validateLogName(name):
    if name is None:
        raise ZeusException("Invalid input. Log name cannot be None.")
    name_length = len(name)
    if name_length < 1 or name_length > 255:
        raise ZeusException("Invalid log name. It must be longer than 1 "
                            "character and shorter than 255 charaters.")
    if not re.match(r"^[a-zA-Z0-9]*$", name):
        raise ZeusException("Invalid log name. It can only contain "
                            "letters or numbers.")


class ZeusException(Exception):
    pass
