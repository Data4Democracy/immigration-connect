GIT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD 2>/dev/null)
GIT_BRANCH_CLEAN := $(shell echo $(GIT_BRANCH) | sed -e "s/[^[:alnum:]]/-/g")
DOCKER_IMAGE := regulationsgov$(if $(GIT_BRANCH_CLEAN),:$(GIT_BRANCH_CLEAN))

DOCKER_BUILD_ARGS ?= --force-rm
DOCKERFILE ?= Dockerfile

DOCKER_ENV := -e DISPLAY=${DISPLAY}
DOCKER_MOUNT := -v $(CURDIR):/opt/app -v /tmp/.X11-unix:/tmp/.X11-unix
DOCKER_FLAGS := docker run --rm -it --net host --security-opt seccomp=chrome.json $(DOCKER_ENV) $(DOCKER_MOUNT)

DOCKER_RUN := $(DOCKER_FLAGS) "$(DOCKER_IMAGE)"

.PHONY: build format shell clean

build:
	docker build $(DOCKER_BUILD_ARGS) -f "$(DOCKERFILE)" -t "$(DOCKER_IMAGE)" .

format:
	yapf -i --style=google

shell: build
	xhost +
	$(DOCKER_RUN) bash

clean:
