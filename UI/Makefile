install:
	install -m 0644 -o root -g root etc/nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
	install -m 0644 -o root -g root htdocs/preview/* -D -t /usr/local/openresty/nginx/html/preview || true
	install -m 0644 -o root -g root htdocs/refview/* -D -t /usr/local/openresty/nginx/html/refview || true
	install -m 0644 -o root -g root htdocs/ssoar/* -D -t /usr/local/openresty/nginx/html/ssoar || true
	install -m 0644 -o root -g root htdocs/ssoar-gold/* -D -t /usr/local/openresty/nginx/html/ssoar-gold || true
	install -m 0644 -o root -g root htdocs/no_preview/* -D -t /usr/local/openresty/nginx/html/no_preview || true
	install -m 0644 -o root -g root htdocs/datasets/* -D -t /usr/local/openresty/nginx/html/datasets || true
	cp -a htdocs/blog/* /usr/local/openresty/nginx/html/blog
	chmod -R 644 /usr/local/openresty/nginx/html/blog/*
	install -m 0644 -o root -g root htdocs/* -D -t /usr/local/openresty/nginx/html || true

restart:
	pkill openresty; /usr/local/openresty/bin/openresty

deploy: install restart
