.DEFAULT_GOAL := help

# Customize these variables as needed
IMAGE := ai-agent
CONTAINER := ai-agent
NETWORK := ai-lab
DATA_VOLUME := ai-agent-data

.PHONY: initialize-environment build run test stop clean execute-command help

initialize-environment: ## intialize docker environment (volumes, networks,...)
	docker volume create $(DATA_VOLUME)

remove-volume: ## remove the data volume
	docker volume rm $(DATA_VOLUME)

build:	## build the image 
	docker build -t $(IMAGE) .

run: ## run the agent
	docker run --rm -it \
		--network $(NETWORK) \
		--name $(CONTAINER) \
		-v $(DATA_VOLUME):/data \
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

execute-command: ## Usage: COMMAND=<quote>ls -la<quote> make execute-command
	docker run --rm -v ai-agent-data:/data python:3.12-slim sh -c '$(COMMAND)'


help:	## list the available targets 
	@echo 'IMAGE = ' $(IMAGE)
	@echo 'CONTAINER = ' $(CONTAINER)
	@sed -rn 's/^([a-zA-Z_-]+):.*?## (.*)$$/"\1" "\2"/p' < $(MAKEFILE_LIST) | xargs printf "make %-25s# %s\n"
