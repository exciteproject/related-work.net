install:
	install -m 0644 -o root -g root etc/nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
	install -m 0644 -o root -g root htdocs/* --t /usr/local/openresty/nginx/html

restart:
	pkill openresty; /usr/local/openresty/bin/openresty

deploy: install restart
