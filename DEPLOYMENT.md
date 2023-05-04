# Deployment:

## Deployment information:
The application will be deployed by BU SAIL into one of their docker application. So far BU SAIL has provided us the predefined
Dockerfile and docker-compose.yml. However, since we are developing a microservice, after BU SAIL retreive our code, they can deploy
our application on anywhere they want as long as they have the requirements that we specify in the requirements.txt installed in the running environment

Dockerfile: https://github.com/hicsail/analytics-microservice/blob/main/Dockerfile  
docker-compose.yml: https://github.com/hicsail/analytics-microservice/blob/main/docker-compose.yml



## Steps:
On Mac:
1. Make sure you have installed docker locally. You can do this by running the following command in a terminal
 ```shell
 docker --version
 ```
2. Install Docker Desktop
3. After installing Docker locally, you need to make sure you Docker daemon is running. You can do this by running the command: 
```shell
brew services list | grep docker
```
4. If Docker is not running, start it with the following command on Mac.  
```shell
brew services start docker
```
5. Start the Docker Desktop
6. Get the application repository by running:  
```shell
Git clone https://github.com/hicsail/analytics-microservice.git
```
7. Go to the root of the analytics-microservice repo by entering:  
```shell
cd analytics-microservice
```
8. Run the following command to build a docker image
```shell
docker build ./
```
9. Run the following command to run the application in Docker
```shell
docker-compose up
```


## Issues:
The predefined Dockerfile and coker-compose.yml has some mismatched information with our application, when you run the Steps above, 
it will have module import error and cannot start a database. This is an issue that need to be handle in the future if BU SAIL decides
to run our application with the predefined Dockerfile and docker-compose.yml contained in the root of our application.
