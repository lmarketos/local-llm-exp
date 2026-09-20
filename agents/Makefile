.DEFAULT_GOAL := help

# Customize these variables as needed
IMAGE := ai-agent
CONTAINER := ai-agent
VOLUME := ai-agent
NETWORK := ai-lab

build:	## build the image 
	docker build -t ai-agent .

run: ## run the agent
	docker run --rm -it \
		--network $(NETWORK) \
		$(CONTAINER)

# Stop the running container
stop: ## stop the container
	docker stop $(CONTAINER) 

# Remove the container and image
clean: ## remove the container and image 
	stop 
	docker rm $(CONTAINER)
	docker rmi $(IMAGE)

help:	## list the available targets 
	@echo 'IMAGE = ' $(IMAGE)
	@echo 'CONTAINER = ' $(CONTAINER)
	@sed -rn 's/^([a-zA-Z_-]+):.*?## (.*)$$/"\1" "\2"/p' < $(MAKEFILE_LIST) | xargs printf "make %-25s# %s\n"
