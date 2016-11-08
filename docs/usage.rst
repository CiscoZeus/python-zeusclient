========
Usage
========

Create a Zeus client
----------------------

To use Zeus Python Client in a project::

    from zeus import client

Create a ZeusClient object::

    z = client.ZeusClient(USER_TOKEN, 'api.ciscozeus.io')

Now you are ready to start sending and querying logs and metrics. :D

Logs
----------------------

Log name format
~~~~~~~~~~~

All log names must have only letter and numbers (A-Za-z0-9).

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

Metric name format
~~~~~~~~~~~

All metric names must start with a letter or number (A-Za-z0-9) and can contain '.', '-' and '_'.

Send Metrics
~~~~~~~~~~~

You can send metrics as an array of timestamps and value dictionaries. To send metrics::

    metrics = [
        {"timestamp": 123541423,
         "point": {"column1": 1, "column2": 2}},
        {"timestamp": 123541424,
         "point": {"column1": 3, "column2": 4}},
        {"timestamp": 123541425,
         "point": {"column1": 5, "column2": 6}}
    ]
    z.sendMetric("<METRIC_NAME>",metrics)

If you omit the "timestamp" field, then current system time will be used as timestamp.

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

Delete metrics
~~~~~~~~~~~

To delete a metric::

    z.deleteMetric('ZeusTest')

This will delete the entire metric from Zeus.

Dates
----------------------

All dates must be in the Unix timestamp format.


Alerts
----------------------

Creating an alert
~~~~~~~~~~~

To create an alert::

    z.createAlert(
        alert_name="alert_name",
        username="username",
        alert_type="metric",
        alert_expression="cpu.value > 20",
        alert_severity="S1",
        field_name="cpu.value",
        emails="john1234@gmail.com",
        status="active",
        notify_period=60
    )

Retrieving all alerts
~~~~~~~~~~~

To retrieve all alerts::

    z.getAlerts()

Modifying an alert
~~~~~~~~~~~

To modify a specific alert::

    z.modifyAlert(
        alert_id=42
        alert_name="alert_name",
        username="username",
        alert_type="metric",
        alert_severity="S1",
        emails="john1234@gmail.com",
        status="active",
        notify_period=60
    )

Retrieving description on a specific alert
~~~~~~~~~~~

To get information on an alert::

    z.getAlert(
        alert_id=25
    )

Deleting an alert
~~~~~~~~~~~

To delete a alert::

    z.deleteAlert(
        alert_id=25
    )

Bulk enabling alerts
~~~~~~~~~~~

To enable alerts::

    z.enableAlerts(
        alert_id_list=[25, 41, 7]
    )

Bulk disabling alerts
~~~~~~~~~~~

To disable alerts::

    z.disableAlerts(
        alert_id_list=[25, 41, 7]
    )

Triggered Alerts
----------------------

Retrieving all triggered alerts
~~~~~~~~~~~

To retrieve triggered alerts::

    z.getTriggeredAlerts()

Retrieving all triggered alerts in the last 24 hours
~~~~~~~~~~~

To retrieve all alerts triggered in the past 24 hours::

    z.getTriggeredAlertsLast24Hours()
