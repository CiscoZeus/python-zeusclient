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


from zeus.client import ZeusClient
import os
import random

ZEUS_API = "http://api.ciscozeus.io"
BATCH_SIZE = 1000
NUMBER_OF_SAMPLES = 1000
auth_data = None


# Interactive Zeus 101. Run python file to see it.
os.system('clear')
print("\nWELCOME to Zeus 101\n")
print("This is a sample App that inserts and retrieves data into zeus.")
print(
    "For the purpose of this example, we will connect to zeus,\nwe will " +
    "send some logs and metrics and finally, we will retrieve them.")

raw_input("Press ENTER when you are ready to continue.")


print("Connecting to zeus...")

token = raw_input("What is your user token? ")

z = ZeusClient(token, ZEUS_API)
print("Zeus client created with user token " + token)


print("\nGreat! We are now ready to start sending and receiving data.")

raw_input("Press ENTER when you are ready to continue.")

os.system('clear')

print("User token: " + token)

print("\nLets now post some logs and metrics.")
print("We are going to send a log " + str(NUMBER_OF_SAMPLES) + " times in " +
      "groups of " + str(BATCH_SIZE) + ".")
print("You can send any JSON as a log. However, in this example, we will" +
      " send a single message.")
message = raw_input("What message would you like to send? ")

# Log sending
print("\nPOST request to http://api.ciscozeus.io/logs/" + token + "/Zeus101")
for i in range(0, NUMBER_OF_SAMPLES, BATCH_SIZE):
    messages = [{"message": message + " - "
                 + str(i + x)} for x in range(0,
                                              min(NUMBER_OF_SAMPLES - i,
                                                  BATCH_SIZE))]
    print "Sending group " + str(i + 1) + ': ' + str(z.sendLog("Zeus101",
                                                               messages))

raw_input("\nLogs sent. Press ENTER to send some metrics.")

# Metric sending
print(
    "\nPOST request to http://api.ciscozeus.io/metrics/" + token + "/Zeus101")
for i in range(0, NUMBER_OF_SAMPLES, BATCH_SIZE):
    metrics = [
        {"point": {"value": random.randint(0, 100)}}
        for x in range(0,
                       min(NUMBER_OF_SAMPLES
                           - i, BATCH_SIZE))]
    print "Sending group " + str(i + 1) + ': ' + str(z.sendMetric("Zeus101",
                                                                  metrics))

raw_input("\nMetrics sent. Press ENTER to continue.")

os.system('clear')
print("User token: " + token)
print(
    "\nCongratulations! You now have some logs and metrics in Zeus. Easy, " +
    "right?")
print("Lets now retrieve 10 logs from Zeus and see if they are what we sent.")
raw_input("\nPress ENTER to get 10 logs.")
os.system('clear')

# Log consumption
print(
    "\nGET request to http://api.ciscozeus.io/logs/" + token + "?log_name=" +
    "Zeus101&limit=10&pattern=" + message + "&attribute_name=message")
status, l = z.getLog('Zeus101', limit=10, attribute_name="message",
                     pattern=message)

if status == 200:
    print("\nLogs:")
    for log in l['result']:
        print(str(log['timestamp']) + ": " + log['message'])
    print("\nThere are currently " + str(l['total']) + " logs in your Zeus " +
          "account that match this query.")
else:
    print("\nThere has been an error retrieving logs. Are the parameters " +
          "correctly formatted?")

raw_input("\nLets now retrieve some metrics from Zeus." +
          " Press ENTER when you are ready.")

# Metric consumption
print(
    "\nGET request to http://api.ciscozeus.io/metrics/" + token + "/_values?" +
    "limit=10&group_interval=1m&aggregator_function=sum&filter_condition=" +
    "'value > 90'&aggregator_column=value&metric_name=Zeus101")
status, m = z.getMetric(limit=10, group_interval='1m',
                        metric_name='Zeus101',
                        aggregator_function='sum',
                        aggregator_column='value',
                        filter_condition='value > 20')
print status
print m

if status == 200:
    print "\n" + m[0]['name'] + "\t" + '\t\t'.join(m[0]['columns'])
    for metric in m[0]['points']:
        print '\t' + '\t'.join(map(str, metric))
else:
    print("There has been an error retrieving metrics. Are the parameters " +
          "correctly formatted?")

raw_input(
    "\nLet's retrieve a list of metric names. " +
    "Press ENTER when you are ready.")

# Metric list consumption
print("\nGET request to http://api.ciscozeus.io/metrics/" +
      token + "/_names?limit=10")
status, m = z.getMetricNames(limit=10)
for metric in m:
    print metric

raw_input("\nFinally let's delete the metric we just inserted. Press ENTER " +
          "to continue.")

print("Deleting...")
print("\nDELETE request to http://api.ciscozeus.io/metrics/" +
      token + "/Zeus101")
z.deleteMetric('Zeus101')

# Metric list consumption
print("\nGET request to http://api.ciscozeus.io/metrics/" +
      token + "/_names?limit=10")
status, m = z.getMetricNames(limit=10)
for metric in m:
    print metric

raw_input(
    "\nThis is the end of Zeus101. Please, feel free to use the ZeusClient " +
    "class as a base for your code. Press ENTER to exit.")
