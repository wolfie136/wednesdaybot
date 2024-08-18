format:
	black src/ utils/
	isort --profile black src/ utils/

lint:
	black --check src/ utils/
	isort --profile black --check src/ utils/
	flake8 src/ utils/
	mypy src/ utils/

test:
	pytest -v --cov --cov-report xml:coverage.xml --cov-report term src/ utils/

deploy:
	sls deploy
