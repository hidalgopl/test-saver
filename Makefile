build:
	docker build -t test_saver:dev .
.PHONY: build

test:
	DATABASE_URL="sqlite:///example.db" python -m pytest
.PHONY: test

deploy_to_cluster:
    helm upgrade -i test-saver chart/test-saver
.PHONY: deploy_to_cluster
