web: env/bin/gunicorn --chdir $APP_HOME/InvenTree -c src/backend/InvenTree/gunicorn.conf.py InvenTree.wsgi -b 0.0.0.0:$PORT
worker: env/bin/python src/backend/InvenTree/manage.py qcluster
cli: echo "" && . env/bin/activate && exec env/bin/python -m invoke
