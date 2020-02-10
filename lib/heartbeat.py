"""Simple heartbeat library"""
import logging
from datetime import timedelta

import requests
import isodate

heartbeat_app_url = "http://localhost:5000/"

__VERSION__ = "0.1"
__AUTHOR__ = "Joshua Coales"
__EMAIL__ = "dr-spangle@dr-spangle.com"
__URL__ = "https://github.com/joshcoales/simple-heartbeat-lib"


def app_url(app_name: str) -> str:
    return f"{heartbeat_app_url}/update/{app_name}"


def update_heartbeat(app_name: str, *, status=None, expiry_period: timedelta):
    try:
        if status is None and expiry_period is None:
            requests.get(app_url(app_name))
        else:
            post_data = {}
            if status is not None:
                post_data['status'] = status
            if expiry_period is not None:
                post_data['expiry'] = isodate.duration_isoformat(expiry_period)
            requests.post(
                app_url(app_name),
                json=post_data
            )
    except Exception as e:
        logger = logging.getLogger("heartbeat-status")
        logger.error("Failed to update status on heartbeat server due to exception", exc_info=e)


def initialise_app(app_name: str, expiry_period: timedelta):
    requests.post(
        app_url(app_name),
        json={"expiry": isodate.duration_isoformat(expiry_period)}
    )
