run:
	python3 app/main.py

test:
	python3 -m pytest -n 2

install:
	pip3 install -r requirements.txt