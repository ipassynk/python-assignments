#!/bin/bash
set -e

/etc/init.d/postgresql start
service rabbitmq-server start
service apache2 start
service cron start

tail -f /dev/null
