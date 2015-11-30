.PHONY: all build test integration-test unit-test

all: test

clean:
	rm -rf tests/__pycache__
	rm -rf tests/*/__pycache__
	docker rm -vf dpy-dind

build:
	docker build -t docker-machine-py .

test: unit-test integration-dind integration-dind-ssl

#unit-test: build
unit-test:
	#docker run docker-py py.test tests/unit
	docker run \
		--rm \
		-v /home/jgrowlands/.docker:/root/.docker \
		-v /home/jgrowlands/Code/github.com/jgrowl/rowlands.io/bootstrap/docker-machine-py:/home/docker-machine-py \
		docker-machine-py py.test tests/unit


#integration-test: build
integration-test:
	#docker run --rm -v /home/jgrowlands/.docker:/root/.docker -v /home/jgrowlands/Code/github.com/jgrowl/rowlands.io/bootstrap/docker-machine-py:/home/docker-machine-py docker-machine-py py.test tests/integration
	docker run \
		--rm \
		-v /home/jgrowlands/.docker:/root/.docker \
		-v /home/jgrowlands/Code/github.com/jgrowl/rowlands.io/bootstrap/docker-machine-py:/home/docker-machine-py \
		docker-machine-py py.test tests/integration

