# Minimum support and confidence (override on the command line,
# e.g. make run SUPPORT=500 CONFIDENCE=0.8)
SUPPORT ?= 1000
CONFIDENCE ?= 0.7

.PHONY: run test clean

# Run Task 1 (A-Priori) and Task 2 (association rules)
run:
	python3 main.py --support $(SUPPORT) --confidence $(CONFIDENCE)

# Run the unit tests
test:
	python3 -m pytest

# Remove Python cache files
clean:
	rm -rf __pycache__ src/__pycache__ tests/__pycache__ .pytest_cache
