#!/usr/bin/env bash

# Activate the virtual environment if present
if [ -d venv ]; then
  source venv/bin/activate;
fi

# 
if [ ! -d migrations ]; then
  flask --app api/wsgi.py db init
fi

#
message=${1}
flask --app api/wsgi.py db migrate -m \""${message}"\"
flask --app api/wsgi.py db upgrade
