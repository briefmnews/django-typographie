install:
	pip install -r test_requirements.txt

test:
	py.test

coverage:
	py.test --cov=typographie typographie/tests

report:
	py.test --cov=typographie --cov-report=html typographie/tests

release:
	git tag -a $(shell python -c "from typographie import __version__; print(__version__)") -m "$(m)"
	git push origin --tags