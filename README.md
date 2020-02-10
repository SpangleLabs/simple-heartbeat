# Simple heartbeat

This repository is 2 parts, a [library](library/README.md) and a [server](server/README.md)

It's just a simple library to ping a simple flask server, and say when the last ping was received.
This allows a liveness check. 
The server can then return an error code when the heartbeat for a given app is too old, 
which can be monitored in other applications like [uptime robot](https://uptimerobot.com).

The best way to get details about this is to read the readme files in the library and server directories.
