install-deps:
	pip install redis pyoai lxml

redis-dropall:
	redis-cli FLUSHALL

redis-show-queue:
	@echo 'LRANGE "celery\x06\x169" 0 -1' | redis-cli | jq '.headers | [.task, .argsrepr]' --compact-output -r

redis-restart:
	sudo service redis restart

celery-start:
	celery -A tasks worker --concurrency=1 -n "%h:$$$$"

flower-start:
	flower -A tasks

pg-user-and-db:
	sudo -u postgres psql -c 'CREATE USER rw WITH PASSWORD "rw";'
	sudo -u postgres psql -c 'CREATE DB rw;'
	sudo -u postgres psql -c 'GRANT ALL ON DATABASE rw to rw;'

pg-tables:
	PGPASSWORD=rw psql -U rw -c 'CREATE TABLE IF NOT EXISTS oa_results(key text PRIMARY KEY, value json);'

pg-results:
	PGPASSWORD=rw psql -U rw -c 'SELECT key FROM oa_results;'
