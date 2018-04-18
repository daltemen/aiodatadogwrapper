import logging

from datadog import statsd, initialize, api
from ..settings import DATADOG_HOST, DATADOG_API_HOST, DATADOG_API_KEY, DATADOG_APP_KEY

logging.getLogger(__name__)


async def initialize_client():
    options = {
        'api_key': DATADOG_API_KEY,
        'app_key': DATADOG_APP_KEY,
        'api_host': DATADOG_API_HOST
    }
    initialize(**options)


async def increment_metric(metric_name):
    statsd.host = DATADOG_HOST
    statsd.increment(metric_name)


async def set_metric(metric_name, value):
    statsd.host = DATADOG_HOST
    statsd.gauge(metric_name, value)


async def send_event(
        title,
        body,
        tag_list,
        alert_type='info',
        priority='normal',
        ):
    await initialize_client()
    try:
        api.Event.create(
            title=title,
            text=body,
            tags=tag_list,
            alert_type=alert_type,
            priority=priority
        )
    except Exception as e:
        logging.exception('The event could not be sent %s', e)
