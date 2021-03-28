#!/usr/bin/env sh

set -o errexit
set -o nounset

echo "DJANGO_ENV is $DJANGO_ENV"
if [ "$DJANGO_ENV" != 'production' ]; then
  echo 'Error: DJANGO_ENV is not set to "production".'
  echo 'Application will not start.'
  exit 1
fi

export DJANGO_ENV

python /code/manage.py migrate --noinput
python /code/manage.py collectstatic --noinput
python /code/manage.py compilemessages
python /code/manage.py initadmin

/usr/local/bin/uwsgi --master \
  --wsgi-file=/code/project/wsgi.py \
  --threads=2 \
  --processes=1 \
  --socket=0.0.0.0:8000  \
  --chdir=/code \
  --http-timeout=180
