#!/bin/sh

set -e

# activate our virtual environment here
. /opt/venv/bin/activate

# You can put other setup logic here

# Evaluating passed command:
exec "$@"
