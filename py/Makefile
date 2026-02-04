VENV = .venv

$(VENV):
	python -m venv $(VENV)

install: $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

run: $(VENV)
	$(VENV)/bin/python main.py

