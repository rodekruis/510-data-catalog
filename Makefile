include .env
.PHONY: build-base-images dev-2.9 base-2.9

MAKEFLAGS += -j2

build-base-images: dev-2.9

dev-2.9: base-2.9
		docker build -t $(CKAN_SERVICE_IMAGE) -f ckan-build/ckan-service/Dockerfile . --build-arg baseImage=${CKAN_BASE_IMAGE} --no-cache

base-2.9:
		docker build -t $(CKAN_BASE_IMAGE) -f ckan-build/ckan/Dockerfile . --no-cache
