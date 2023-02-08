# !/bin/bash
echo "SERVICE RUN STATUS: ONLINE !!!"


cd $(dirname $0)/..


cd app
nohup celery -A manage.celery worker -Q main_queue -l info -f /czt_web_api/logs/celery.log &
gunicorn app:app -c configs/gunicorn_conf.py
