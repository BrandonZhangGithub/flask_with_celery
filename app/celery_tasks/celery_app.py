from initialization import create_app, make_celery

app = create_app()
celery = make_celery(app)

# celery -A celery_tasks.celery_app.celery beat -l info
# celery -A celery_tasks.celery_app.celery worker -Q main_queue -l info