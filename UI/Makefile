install:
	install -m 0644 -o root -g root etc/nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
	install -m 0644 -o root -g root htdocs/preview/* -D -t /usr/local/openresty/nginx/html/preview || true
	install -m 0644 -o root -g root htdocs/refview/* -D -t /usr/local/openresty/nginx/html/refview || true
	install -m 0644 -o root -g root htdocs/ssoar/* -D -t /usr/local/openresty/nginx/html/ssoar || true
	install -m 0644 -o root -g root htdocs/search/* -D -t /usr/local/openresty/nginx/html/search || true
	install -m 0644 -o root -g root htdocs/* -D -t /usr/local/openresty/nginx/html || true

restart:
	pkill openresty; /usr/local/openresty/bin/openresty

deploy: install restart
