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

pg-user-and-db:
	psql -U postgres -c 'CREATE USER rw WITH PASSWORD "rw";'
	sudo -U postgres -c 'CREATE DB rw;'
	sudo -U postgres -c 'GRANT ALL ON DATABASE rw to rw;'

pg-tables:
	@# psql -U rw -c 'CREATE TABLE IF NOT EXISTS oa_results(key TEXT PRIMARY KEY, value JSON);'
	@#psql -U rw -c 'CREATE TABLE IF NOT EXISTS meta(meta_id VARCHAR(50) PRIMARY KEY, author TEXT, title TEXT, abstract TEXT, info TEXT, subject TEXT, year INTEGER);'

pg-results:
	psql -U rw -c 'SELECT key FROM oa_results;'
