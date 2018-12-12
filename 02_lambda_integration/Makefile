.PHONY: help
.DEFAULT_GOAL := help
environment = "example"

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

create: lambda-dist ## create env
	@sceptre launch-env $(environment)

delete: ## delete env
	@sceptre delete-env $(environment)

info: ## describe resources
	@sceptre describe-stack-outputs $(environment) tour-of-heroes

lambda-build-zip: ## build the lambda
	docker build -t my-lambda .

lambda-dist: lambda-build-zip ## create a new lambda.zip in 'dist' directory
	mkdir -p dist
	./copy_from_docker.sh

clean: ## clean
	rm -rf dist

merge-swagger: ## merged swagger with api gateway
	@aws-cfn-update \
		rest-api-body  \
		--resource RestAPI \
		--open-api-specification swagger/swagger.yaml \
		--api-gateway-extensions swagger/aws-extensions.yaml \
		--add-new-version \
		templates/tour-of-heroes.yaml