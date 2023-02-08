from initialization import create_app
from initialization import make_celery

app = create_app()
celery = make_celery(app)