all: build


build: render


render:
	make -C notes

prod-render:
	make -C notes PELICAN_CONFIG=../prod.py

upload: prod-render
	cd output; \
	rsync -vr --delete \
		. \
		tag@pault.ag:/srv/www/nginx/notes/


.PHONY: render build all upload
