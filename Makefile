help: ## Show this text.
	# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all test clean help

all:
	@true

test:
	sam validate

clean:
	@rm -f packaged.yaml

##### AWS SAM

.PHONY: release-sam

release-sam: template.yaml lambda/macro.py lambda/resource.py ## Release the application to AWS Serverless Application Repository
	sam package \
		--template-file template.yaml \
		--output-template-file packaged.yaml \
		--s3-bucket shogo82148-sam
	sam publish \
		--template packaged.yaml \
		--region us-east-1
