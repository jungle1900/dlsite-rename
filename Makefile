.PHONY: run build

run:
	py .\main.py

build:
	pyinstaller -F -c main.py
	cp .\config.yaml .\dist\
