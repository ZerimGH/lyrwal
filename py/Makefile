VENV = .venv

$(VENV):
	python -m venv $(VENV)

all: $(VENV)

install: $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt
	mkdir -p ~/.lyrwal
	cp -r . ~/.lyrwal/py

.PHONY: all
