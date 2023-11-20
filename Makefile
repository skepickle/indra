.PHONY: clean run
clean:
	@find . -depth -type d -name __pycache__ -exec rm -r {} \;
run:
	#@python3 -m indra
	@python3 vritrasura.py
