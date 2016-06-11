.PHONY: all build test integration-test unit-test

all: test

clean:
	rm -rf tests/__pycache__
	rm -rf tests/*/__pycache__

build:
	docker build -t docker-machine-py .

test: unit-test integration-test

unit-test: build
	docker run --rm docker-machine-py py.test tests/unit

integration-test: build
	docker run -v /var/run/docker.sock:/var/run/docker.sock --rm docker-machine-py py.test tests/integration
