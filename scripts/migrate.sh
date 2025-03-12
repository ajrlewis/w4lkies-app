#!/usr/bin/env bash

# Activate the virtual environment if present
if [ -d venv ]; then
  source venv/bin/activate;
fi

# 
if [ ! -d migrations ]; then
  pwd
  ls
  python3 -m flask --app api/wsgi.py db init
fi

#
message=${1}
python3 -m flask --app api/wsgi.py db migrate -m \""${message}"\"
python3 -m flask --app api/wsgi.py db upgrade
