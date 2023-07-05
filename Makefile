.PHONY: init lint run clean

init:
	pip install -r requirements-dev.txt

lint: init
	black .
	flake8 --config .flake8 .

run: lint
	python main.py

clean:
	@find . -type d -name "logs" -exec rm -rf {} +
	@find . -type d -name "__pycache__" -exec rm -rf {} +
