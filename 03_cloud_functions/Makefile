.PHONY: help
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

create: ## create the cloud function
	gcloud functions deploy hero_service --runtime python37 --trigger-http

delete: ## delete the cloud function
	gcloud functions delete hero_service

info: ##
	gcloud functions describe hero_service