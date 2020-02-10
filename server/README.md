# Simple heartbeat server

This is what it says. 
This is a simple heartbeat server I've built, such that a simple request can update an application 
(or thread) status, and a simple watcher, like [uptime robot](http://uptimerobot.com/) can notify 
when an app hasn't registered a heartbeat for a while.

## Usage
You can manually call these endpoints, or use the [simple heartbeat library](https://github.com/joshcoales/simple-heartbeat-lib)
### Update status
To update status, simply make a request to the `/update/<app_name>` endpoint, for whatever given 
app name.
App names can be created on the fly.

By default, this will set the status to "online", or whatever the last status was. Status can be 
any string, although "offline" will cause the check to return a 503 error for monitoring purposes.
This also sets the expiry period to 5 minutes from the last heartbeat by default, or to the last 
heartbeat's expiry period.

To specify a custom status or expiry period, POST a json document to the update endpoint for your 
specified app name, with the keys: 
- "status": a string, representing application status.
- "expiry": an ISO-8601 formatted duration, until the heartbeat should be considered expired.


### Check status
To check status, simply check the `/check/<app_name>` endpoint. If the heartbeat has expired, or 
the latest status was "offline", a 503 error will be returned. Otherwise some information on the 
last status update will be given.


## Docker deployment
This should be available on docker hub, at [joshcoales/simple-heartbeat](https://hub.docker.com/joshcoales/simple-heartbeat)
and can be deployed like so:
```shell script
docker run \
  --name=heartbeat_server \
  --restart=always \
  --volume=/etc/heartbeat/config/:/app/config/ \
  -p 80:5000 \
  -d joshcoales/simple-heartbeat 
``` 
