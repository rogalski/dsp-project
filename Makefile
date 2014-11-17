PYTHON_FILES=main.py blocks
PROJECT_NAME=rogalski_131385

all: clean prerequisites lint uml

prerequisites:
	pip install -r requirements.txt

clean:
	rm -f *.png *.pyc

uml:
	pyreverse $(PYTHON_FILES) -o png -p $(PROJECT_NAME) -AS

pep8:
	pep8 $(PYTHON_FILES)

pylint:
	pylint $(PYTHON_FILES) --disable=C,R

lint: pep8 pylint
