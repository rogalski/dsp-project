PYTHON_FILES=main.py utils.py plots.py blocks system
PROJECT_NAME=lrogalski

all: clean prerequisites lint

prerequisites:
	pip install -r requirements.txt

clean:
	rm -f *.png *.pyc

uml:
	pyreverse $(PYTHON_FILES) -o png -p $(PROJECT_NAME) -AS

pep8:
	pep8 $(PYTHON_FILES)

pylint:
	pylint $(PYTHON_FILES) --disable=C

lint: pep8 pylint
