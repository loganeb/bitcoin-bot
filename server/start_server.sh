#!/bin/bash

export PYTHONPATH="../common/"
export FLASK_APP="server.py"
export FLASK_ENV=development

source "../venv/bin/activate"

flask run
