#!/bin/bash
cd /export/home/dkostic/related-work.net
source py3env/bin/activate
cd DataImport/
export PYTHONPATH=./tools
flower -A capp --port=8099