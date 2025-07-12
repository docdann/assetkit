.PHONY: install test package clean

install:
	pip install -e .

test:
	pytest -q

package:
	python -m build

clean:
	rm -rf build dist *.egg-info
