.DEFAULT_GOAL := help

# Customize these variables as needed
IMAGE := ai-agent
CONTAINER := ai-agent
NETWORK := ai-lab

.PHONY: build run test stop clean help

build:	## build the image 
	docker build -t $(IMAGE) .

run: ## run the agent
	docker run --rm -it \
		--network $(NETWORK) \
		--name $(CONTAINER) \
		$(CONTAINER)

# Stop the running container
stop: ## stop the container
	-docker stop $(CONTAINER) 

# Remove the container and image
clean: ## remove the container and image 
	-stop 
	-docker rm $(CONTAINER)
	-docker rmi $(IMAGE)

test: ## run tests
	docker run --rm \
		--network $(NETWORK) \
		$(IMAGE) \
		pytest --cov=agent --cov-report=term-missing


help:	## list the available targets 
	@echo 'IMAGE = ' $(IMAGE)
	@echo 'CONTAINER = ' $(CONTAINER)
	@sed -rn 's/^([a-zA-Z_-]+):.*?## (.*)$$/"\1" "\2"/p' < $(MAKEFILE_LIST) | xargs printf "make %-25s# %s\n"
