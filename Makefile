build:
	docker build -t test_saver:dev .
.PHONY: build

test:
	DATABASE_URL="sqlite:///example.db" python -m pytest
.PHONY: test
