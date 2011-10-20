
.PHONY: default all clean flush re archives delivery %.pdf

.SECONDARY: graph.svg

.SUFFIXES: .dot .neato .png .gif

default: all

clean:
	rm -f *~
#	rm -f *.pdf
#	rm -f *.dot

flush: clean
#	rm -f *.png

re: flush all

all:
	$(MAKE) $$(for i in *.csv; do echo $$(basename $$i ".csv").pdf; done)

archives:
	zip package.zip *.png *.dot makefile *.txt *.pdf

delivery: re archives

# We add the rendering script here to be sure we 
%.svg: %.py ziv.py
	./ziv.py $< $@

%.png: %.svg
#	/usr/local/bin/convert -size 500x500 $< $@
	/usr/local/bin/convert -size 500x500 -density 50x50 $< $@
	open $@

%.pdf: %.svg
	/usr/local/bin/convert -size 500x500 $< $@
	open $@
