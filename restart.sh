#!/usr/bin/env bash
echo "Restarting services..."
./ember-front/build.sh &&
. venv/bin/activate &&
./server/manage.py collectstatic &&
deactivate &&
service rc.local restart &&
service nginx restart
echo "Finished restart"