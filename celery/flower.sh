#!/bin/bash
cd /EXCITE/celery
source py3env/bin/activate
cd DataImport/
export PYTHONPATH=./tools
flower -A capp --port=8099