PYTHON_FILES=main.py utils.py plots.py blocks system
PROJECT_NAME=lrogalski

all: clean prerequisites lint

prerequisites:
	# pip install -r requirements.txt

clean:
	rm -rf _output __pycache__ *.png *.pyc

uml:
	pyreverse $(PYTHON_FILES) -o png -p $(PROJECT_NAME) -AS

pep8:
	python3-pep8 $(PYTHON_FILES) --max-line-length=119

pylint:
	python3-pylint $(PYTHON_FILES) --disable=C

lint: pep8 pylint
