.PHONY: help
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

create: ## deploys the application
	gcloud app deploy

browse: ## open browser
	gcloud app browse

logs: ## show logs
	gcloud app logs tail -s default

info: ## displays data about the app
	gcloud app describe

list: ## list app engine instances
	gcloud app instances list

run: ## run locally
	pipenv run python main.py