.PHONY: all flakes test tests clean coverage

all: flakes tests

flakes:
	pyflakes yelp_encodings tests setup.py

test_venv: requirements.txt
	rm -rf test_venv
	virtualenv test_venv
	bash -c 'source test_venv/bin/activate && \
	    pip install -r requirements.txt'

test: tests
tests: flakes test_venv
	bash -c "source test_venv/bin/activate && testify tests"

clean:
	rm -rf test_venv
	find . -iname '*.pyc' -delete
