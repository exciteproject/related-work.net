install-deps:
	pip install -r requirements.txt

jobs-worker-start:
	celery -A capp worker --concurrency=1 -n "%h:$$$$"

jobs-ui:
	flower -A capp

jobs-clear-all:
	redis-cli FLUSHALL

jobs-show-queue:
	@echo 'LRANGE "celery\x06\x169" 0 -1' | redis-cli | jq '.headers | [.task, .argsrepr]' --compact-output -r
