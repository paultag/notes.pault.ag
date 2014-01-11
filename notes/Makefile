.SUFFIXES:
.SUFFIXES: .md .html

PELICAN = pelican
PELICAN_OUTPUT = ../output
PELICAN_CONFIG = ../conf.py
PELICAN_FLAGS = -v
PELICAN_THEME = ../themes
PELICAN_CONTENT = .

THEME = epipe

all: build


build: theme render


theme:
	make -C $(PELICAN_THEME)/$(THEME)


render:
	$(PELICAN) -o $(PELICAN_OUTPUT) \
		-s $(PELICAN_CONFIG) \
		-t $(PELICAN_THEME)/$(THEME) \
		$(PELICAN_CONTENT) \
		$(PELICAN_FLAGS)


.PHONY: build theme
