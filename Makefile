IMAGE_NAME = mongodb

MODULEMDURL=file://mongodb.yaml

default: run 

build:
	docker build --tag=$(IMAGE_NAME) .

run: build
	docker run -d $(IMAGE_NAME)

test: build
	cd tests; MODULE=docker MODULEMD=$(MODULEMDURL) URL="docker=$(IMAGE_NAME)" make all
#        cd tests; MODULE=rpm MODULEMD=$(MODULEMDURL) URL="docker=$(IMAGE_NAME)" make all
