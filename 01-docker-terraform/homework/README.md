1. Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container.

What's the version of pip in the image?

docker run -it --rm --entrypoint=bash python:3.13

pip -V 

Version is 25.3

2. Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

Since the two containers are on the same network, they can see each other. Therefore, pgadmin should connect to the postgres database with db:5432 because the second port number is the container port. 

3. 