#!/usr/bin/env bash

source .env
source venv/bin/activate
python3 api/wsgi.py 0.0.0.0 42069
