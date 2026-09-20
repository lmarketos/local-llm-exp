.DEFAULT_GOAL := help

# Customize these variables as needed
IMAGE := ollama/ollama:latest
CONTAINER := ollama
VOLUME := ollama
NETWORK := ai-lab

initialize-environment: ## intialize docker environment (volumes, networks,...)
	docker volume create $(VOLUME)
	docker network create $(NETWORK)

create:	## create and run the container 
	docker run -d \
          --name $(CONTAINER)\
	  --gpus all \
	  --network $(NETWORK) \
	  -v $(VOLUME):/root/.$(CONTAINER) \
	  $(IMAGE)

start: ## start the existing container
	docker start $(CONTAINER)


# Stop the running container
stop: ## stop the container
	docker stop $(CONTAINER) 

# Remove the container and image
clean: ## remove the container and image 
	stop 
	docker rm $(CONTAINER)
	docker rmi $(IMAGE)

install-qwen3: ## install the qwen3 model in the container
	docker exec -it ollama ollama pull qwen3:8b

help:	## list the available targets 
	@echo 'IMAGE = ' $(IMAGE)
	@echo 'CONTAINER = ' $(CONTAINER)
	@sed -rn 's/^([a-zA-Z_-]+):.*?## (.*)$$/"\1" "\2"/p' < $(MAKEFILE_LIST) | xargs printf "make %-25s# %s\n"
