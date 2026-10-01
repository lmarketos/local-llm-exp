.DEFAULT_GOAL := help

# Customize these variables as needed
RUNTIME_IMAGE := ai-agent
RUNTIME_CONTAINER := ai-agent
DEBUG_IMAGE := ai-agent-debug
DEBUG_CONTAINER := ai-agent-debug
NETWORK := ai-lab
DATA_VOLUME := ai-agent-data

.PHONY: initialize-environment build run test stop clean execute-command help

initialize-environment: ## intialize docker environment (volumes, networks,...)
	docker volume create $(DATA_VOLUME)

remove-volume: ## remove the data volume
	docker volume rm $(DATA_VOLUME)

build:	## build the image 
	docker build --target base -t $(RUNTIME_IMAGE) .
	docker build --target dev -t $(DEBUG_IMAGE) .

run: ## run the agent
	docker run --rm -it \
		--network $(NETWORK) \
		--name $(RUNTIME_CONTAINER) \
		-v $(DATA_VOLUME):/data \
		-v ./workspace:/data/workspace \
		$(RUNTIME_CONTAINER)

# Stop the running container
stop: ## stop the container
	-docker stop $(RUNTIME_CONTAINER) 

# Remove the container and image
clean: ## remove the container and image 
	-stop 
	-docker rm $(RUNTIME_CONTAINER)
	-docker rmi $(RUNTIME_IMAGE)
	-docker rm $(DEBUG_CONTAINER)
	-docker rmi $(DEBUG_IMAGE)

test: ## run tests
	docker run --rm \
		--network $(NETWORK) \
		$(DEBUG_IMAGE) \
		pytest --cov=agent --cov-report=term-missing

execute-command: ## Usage: COMMAND=<quote>ls -la<quote> make execute-command
	docker run --rm -v ai-agent-data:/data \
		-v ./workspace:/data/workspace \
	$(DEBUG_IMAGE) sh -c '$(COMMAND)'


help:	## list the available targets 
	@echo 'IMAGE = ' $(RUNTIME_IMAGE)
	@echo 'CONTAINER = ' $(RUNTIME_CONTAINER)
	@sed -rn 's/^([a-zA-Z_-]+):.*?## (.*)$$/"\1" "\2"/p' < $(MAKEFILE_LIST) | xargs printf "make %-25s# %s\n"
