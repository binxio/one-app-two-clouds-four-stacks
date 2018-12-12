.PHONY: help
.DEFAULT_GOAL := help
environment := example

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

init: ##
	npm install
#	npm install --save-dev @angular-devkit/build-angular

run: ##
	ng serve --open

dist: ##
	ng build --prod=true
	cp src/error.html dist

clean: ##
	rm -rf dist
	
