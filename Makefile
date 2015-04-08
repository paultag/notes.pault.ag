all: build


build: render static


render:
	make -C notes

prod-render:
	make -C notes PELICAN_CONFIG=../prod.py

static:
	mkdir output/static -p
	cp static/* output/static

upload: prod-render static
	cd output; \
	rsync -vr --delete \
		. \
		tag@pault.ag:/srv/www/sites/notes.pault.ag/


.PHONY: render build all upload static
