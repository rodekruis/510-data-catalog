.PHONY: build-base-images dev-2.9 base-2.9

MAKEFLAGS += -j2

build-base-images: dev-2.9

dev-2.9: base-2.9
	docker build -t ckanbase.azurecr.io/ckan-510:latest -f ckan-build/ckan-service/Dockerfile . --no-cache

base-2.9:
	docker build -t ckanbase.azurecr.io/ckan-base-2.9.3:base -f ckan-build/ckan/Dockerfile . --no-cache
