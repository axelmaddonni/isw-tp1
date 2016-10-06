all: informe

informe: informe.tex
	pdflatex informe.tex
	pdflatex informe.tex

view:
	zathura informe-primera-entrega.pdf

open:
	make && make view

clean:
	rm -f *.aux *.log *.synctex.gz *.out *.xml *.bcf *.blg *.bbl *.toc
