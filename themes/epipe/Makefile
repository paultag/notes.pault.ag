#
#


all: clean build
	@echo "built theme epipe"


clean:
	@echo "removing static"
	@rm -vrf static


build: less resources


resources: less
	mkdir -p static/font static/css static/images
	cp resources/font/* static/font
	cp resources/css/* static/css
	cp resources/images/* static/images


less:
	make -C less
	mkdir -p static/css
	mv less/epipe.css static/css


.PHONY: build clean resources less
