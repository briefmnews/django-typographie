install:
	pip install -r test_requirements.txt

test:
	py.test

coverage:
	py.test --cov=typographie typographie/tests

report:
	py.test --cov=typographie --cov-report=html typographie/tests
