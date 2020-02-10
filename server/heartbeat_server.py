"""Simple heartbeat server"""
import json
from abc import ABC
from datetime import datetime, timedelta
from typing import List, Dict

import flask
import dateutil
import isodate

__VERSION__ = "0.1.0"
__AUTHOR__ = "Joshua Coales"
__EMAIL__ = "dr-spangle@dr-spangle.com"
__URL__ = "https://github.com/joshcoales/simple-heartbeat-lib"

app = flask.Flask(__name__)

default_status = "online"
default_period = isodate.parse_duration("PT5M")


class AppStatus:
    OFFLINE = "offline"

    def __init__(
        self, app_name: str, status: str, timestamp: datetime, expiry: timedelta
    ):
        self.app_name = app_name
        self.status = status
        self.timestamp = timestamp
        self.expiry = expiry

    def __str__(self):
        expiry_timestamp = self.timestamp + self.expiry
        return \
            f'App "{self.app_name}" last reported status as "{self.status}" ' \
            f'at {self.timestamp.isoformat()}. ' \
            f'It has an expiry period of {isodate.duration_isoformat(self.expiry)}. ' \
            f'It will expire at {expiry_timestamp.isoformat()}.'

    def is_expired(self):
        expiry_timestamp = self.timestamp + self.expiry
        return datetime.now() > expiry_timestamp


class DataStore(ABC):
    def __init__(self):
        self.app_status = {}  # type: Dict[str, AppStatus]

    def list_applications(self) -> List[str]:
        return list(self.app_status.keys())

    def get_status(self, app_name: str) -> AppStatus:
        return self.app_status.get(app_name)

    def update_status(self, app_name: str, status: AppStatus):
        if (
            app_name not in self.app_status
            or self.app_status[app_name].timestamp < status.timestamp
        ):
            self.app_status[app_name] = status


class JsonDataStore(DataStore):
    FILE_NAME = "heartbeat_data_store.json"

    def __init__(self):
        super().__init__()
        self._load_from_json()

    def update_status(self, app_name: str, status: AppStatus):
        super().update_status(app_name, status)
        self._save_to_json()

    def _load_from_json(self):
        try:
            with open(self.FILE_NAME, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        for app_name, app_data in data.items():
            status = AppStatus(
                app_name,
                app_data["status"],
                dateutil.parser.parse(app_data["timestamp"]),
                isodate.parse_duration(app_data["expiry_period"]),
            )
            self.app_status[app_name] = status

    def _save_to_json(self):
        json_dict = {}
        for app_name, app_status in self.app_status.items():
            json_dict["app_name"] = {
                "status": app_status.status,
                "timestamp": app_status.timestamp.isoformat(),
                "expiry_period": isodate.duration_isoformat(app_status.expiry),
            }
        with open(self.FILE_NAME, "w") as f:
            json.dump(f, json_dict)


data_store = JsonDataStore()


@app.route("/")
def list_apps():
    return "Apps being watched: {}".format(data_store.list_applications())


@app.route("/update/<app_name>", methods=["GET", "POST"])
def update_status(app_name):
    # Defaults
    new_status = default_status
    new_expiry = default_period
    # Old status, if applicable
    old_status = data_store.get_status(app_name)
    if old_status is not None:
        new_status = old_status.status
        new_expiry = old_status.expiry
    # Post data, if applicable
    req_json = flask.request.get_json(silent=True)
    if req_json is not None:
        new_status = req_json.get("status")
        new_expiry = isodate.parse_duration(req_json.get("expiry"))
    status = AppStatus(app_name, new_status, datetime.now(), new_expiry)
    data_store.update_status(app_name, status)


@app.route("/check/<app_name>")
def check_status(app_name):
    status = data_store.get_status(app_name)
    if status is None:
        flask.abort(404)
    if status.status == status.OFFLINE:
        flask.abort(503, description="This application has reported an offline status")
    if status.is_expired():
        flask.abort(503, description="Heartbeat for this application has expired")
    return str(status)


if __name__ == '__main__':
    app.run()
