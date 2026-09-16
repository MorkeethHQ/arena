BOUT ?= examples/BOUT-002/bout.json

.PHONY: card smoke

card:
	python3 scripts/render_card.py $(BOUT)

smoke:
	python3 -m unittest discover -s tests -v
