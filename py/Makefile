VENV = .venv

$(VENV):
	python -m venv $(VENV)

install: $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt
