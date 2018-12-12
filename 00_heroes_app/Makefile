.PHONY: help
.DEFAULT_GOAL := help
environment := example

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

create: ## create env
	@sceptre launch-env $(environment)

delete: ## delete env
	@sceptre delete-env $(environment)

info: ## describe resources	
	sceptre describe-stack-outputs example heroes 

describe: ## describe the stack outputs
	sceptre describe-stack-outputs $(environment) heroes

cp: clean dist ## copy webapp to bucket
	aws s3 sync tour-of-heroes/dist s3://`sceptre --output json describe-stack-outputs example heroes | jq -r '.[] | select(.OutputKey=="DeployBucket") | .OutputValue'`

dir: # show contents of the bucket
	aws s3 ls s3://`sceptre --output json describe-stack-outputs example heroes | jq -r '.[] | select(.OutputKey=="DeployBucket") | .OutputValue'`

clean: ## clean
	aws s3 rm --recursive s3://`sceptre --output json describe-stack-outputs example heroes | jq -r '.[] | select(.OutputKey=="DeployBucket") | .OutputValue'`

dist: ##
	./make_dist.sh