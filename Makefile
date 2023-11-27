include .env
.PHONY: build-base-images dev-2.10 base-2.10

MAKEFLAGS += -j2

build-base-images: dev-2.10

dev-2.10: base-2.10
		docker build -t $(CKAN_SERVICE_IMAGE) -f ckan-build/ckan-service/Dockerfile . --build-arg baseImage=${CKAN_BASE_IMAGE} --progress=plain

base-2.10:
		docker build -t $(CKAN_BASE_IMAGE) -f ckan-build/ckan/Dockerfile .
