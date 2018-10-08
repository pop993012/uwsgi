from flask  import Flask
from celery import Celery
import configa

app = Flask(__name__)
celery_server=Celery(__name__,include=['task'])
celery_server.config_from_object(configa)


if __name__ == '__main__':
    app.run(port=9001)