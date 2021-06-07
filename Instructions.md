# Setup

Install the CE version of the docker:
```
https://docs.docker.com/engine/install/
```

and, install the docker-compose:
```
https://docs.docker.com/compose/install/
```

## Run the project

> Before running the project, create a file named ```.env```. Use the ```.env.example``` file as a reference.

```
docker-compose up
```

Access the following address: ```http://0.0.0.0:8000/``` or ```http://localhost:8000/```.

# Test

To run the tests, access the **car_manager** container using the command (in another terminal instance, because the last command is showing the log of container):

```shell
docker exec -it car_manager bash
```
Then, inside of the container, run:

```shell
cd solution && python manage.py test
```
