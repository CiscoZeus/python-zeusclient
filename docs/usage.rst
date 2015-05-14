========
Usage
========

Create a Zeus client
----------------------

To use Zeus Python Client in a project::

    import zeus

Create a ZeusClient object::

    z = client.ZeusClient(USER_TOKEN, 'api.ciscozeus.io')

Now you are ready to start sending and querying logs and metrics. :D

Logs
----------------------

Send logs
~~~~~~~~~~~

You can send any key/value pair as a log. To send logs::

    logs = [
        {"message": "My Test Log"},
        {"message": "My Second Test Log"}
    ]
    z.sendLog("<LOG_NAME>",logs)

Query logs
~~~~~~~~~~~

To query logs::

    z.getLog('<LOG_NAME>',
              pattern='*',
              from_date=123456789,
              to_date=126235344235,
              offset=23,
              limit=10)


Metrics
----------------------

Send Metrics
~~~~~~~~~~~

You can send metrics as an array of timestamps and value dictionaries. To send metrics::

    metrics = [{"timestamp": 123541423, "value": 0},
               {"timestamp": 123541424, "value": 1},
               {"timestamp": 123541425, "value": 2.0}
    ]
    z.sendMetric("<METRIC_NAME>",metrics)

Query metric names
~~~~~~~~~~~

To query metric names::

    z.getMetricNames(metric_name="<METRIC_NAME>", limit=10)

Query metrics
~~~~~~~~~~~

To query metrics::

    z.getMetric(metric_name='ZeusTest',
                aggregator='sum',
                from_date=123456789,
                to_date=126235344235,
                group_interval='1m',
                filter_condition='value > 90',
                limit=10)

Dates
----------------------

All dates must be in the Unix timestamp format.
