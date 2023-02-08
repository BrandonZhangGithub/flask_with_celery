#!/bin/bash
cd $(dirname $0)/..
cd app
nohup celery -A manage.celery beat -l info -f /czt_web_api/logs/celery.log &
celery -A manage.celery worker -Q main_queue -l info -f /czt_web_api/logs/celery.log