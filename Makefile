
.PHONY: all
all: venv test

.PHONY: venv
venv:
	tox -e venv

.PHONY:tests test
tests: test
test:
	tox

install-hooks:
	tox -e pre-commit

.PHONY: clean
clean:
	find . -iname '*.pyc' | xargs rm
	rm -rf .tox
