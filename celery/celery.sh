#!/bin/bash
cd /EXCITE/celery
source py3env/bin/activate
cd DataImport/
export PYTHONPATH=./tools
celery -A capp worker --concurrency=4