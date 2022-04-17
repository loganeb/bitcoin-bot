#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export PYTHONPATH="$SCRIPT_DIR/common"

source "$SCRIPT_DIR/venv/bin/activate"

cd "$SCRIPT_DIR/bot" && python bot.py