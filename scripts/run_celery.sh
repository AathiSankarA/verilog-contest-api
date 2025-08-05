# activate virtual environment
source ./env/bin/activate

# install requirements
celery -A Application.worker.celery worker -l info

# deactivate environment
deactivate

