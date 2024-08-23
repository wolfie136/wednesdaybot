format:
	black src/ utils/ tests/
	isort --profile black src/ utils/ tests/

lint:
	black --check src/ utils/ tests/
	isort --profile black --check src/ utils/ tests/
	flake8 src/ utils/ tests/
	mypy src/ utils/ tests/

test:
	pytest -v --cov --cov-report xml:coverage.xml --cov-report term tests/

deploy:
	sls deploy
