# Apache Kafka Hands-on
In this tutorial you will learn:
1. How to set up a single Kafka instance
2. How to handle data in Kafka
4. How to set up a cluster of Kafka nodes
## Requirements
- Docker (https://docs.docker.com/get-docker)

## Step 1: Create a directory or clone the project
Create a directory named kafka and enter the directory (this will be your working directory). If you have cloned this git repository, you can skip this step.
```sh
mkdir kafka
cd kafka
```

## Step 2: Define a single Kafka node
Create a docker-compose file `docker-compose.yml` where you will define the docker container for one single instance of Kafka.

Apacha Kafka depends on Zookeeper to manage the running jobs.

The `docker-compose.yml` should look like this (you can use any text editor like `vi`, `nano` and `WordPad` or GUI to write the compose file). You can find an example in [docker-compose-single.yml](docker-compose-single.yml) or do `cp docker-compose-single.yml docker-compose.yml` (if you have cloned the git repo):
```yml
version: '3'

networks:
  tutorial:
    name: tutorial

services:
  zookeeper:
    image: zookeeper
    networks:
      - tutorial
    ports:
      - target: 2181
        published: 2181
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ALLOW_ANONYMOUS_LOGIN: "yes"

  kafka1:
    image: confluentinc/cp-kafka
    depends_on:
      - zookeeper
    networks:
      - tutorial
    ports:
      - "9092:9092"
      - "19092:19092"
    environment:
      KAFKA_BROKER_ID: 1
      ALLOW_PLAINTEXT_LISTENER: "yes"
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,HOST:PLAINTEXT
      KAFKA_LISTENERS: INTERNAL://0.0.0.0:19092,HOST://0.0.0.0:9092
      KAFKA_ADVERTISED_LISTENERS: HOST://localhost:9092,INTERNAL://kafka1:19092
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```
Save the file and close the editor.

You have created a docker-compose file where you have defined one containerised service of Kafka, using the last Kafka image from DockerHub. The container has the port 27027 opened and mapped to the internal port 27027 of Kafka. It is also connected to a network called *tutorial* . You will later use the network to connect more services together.

## Step 3: Let's run Kafka
To run the Kafka instance using Docker (using `-d` to detach the container from the terminal). The docker compose file must be named `docker-compose.yml`
```sh
docker compose up -d
```

From DockerDesktop you can see if the container is running:
![One MongoDB instance running](one_instance_dockerdesktop.png "One MongoDB instance running")

Another alternative is to use the terminal. To check the running projects in docker, you can use the following. It lists the project and the number of containers, in this case, it will show only 1 container.
```sh
docker compose ls
```

You should see something like:

```
NAME                STATUS              CONFIG FILES
kafka               running(2)          D:\teckna\big-data-workshop\kafka\docker-compose.yml
```

To list the containers and see more information such as their state:

```sh
docker compose ps
```

You should see something like:
```
NAME                IMAGE                   COMMAND                  SERVICE             CREATED             STATUS              PORTS
kafka-kafka-1       confluentinc/cp-kafka   "/etc/confluent/dock…"   kafka               11 minutes ago      Up 11 minutes       0.0.0.0:9092->9092/tcp, 0.0.0.0:19092->19092/tcp
kafka-zookeeper-1   zookeeper               "/docker-entrypoint.…"   zookeeper           11 minutes ago      Up 11 minutes       2888/tcp, 3888/tcp, 0.0.0.0:2181->2181/tcp, 8080/tcp
```

## Step 4: Check connection to Kafka
Let's check if we can connect by opening an interactive shell (you may need to wait until Kafka finishes the set-up and starts accepting connections):

First, to create a topic:
```docker
docker exec -it kafka-kafka-1 /bin/kafka-topics --create --replication-factor 1 --partitions 1 --topic test --bootstrap-server kafka:19092
```
Then, you will need to open two terminals, one for producing messages and other for consuming.

To produce messages:
```docker
docker exec -it kafka-kafka-1 /bin/kafka-console-producer --topic test --bootstrap-server kafka:19092
```

To consume messages (it can take a couple of minutes until it starts consuming messages):
```docker
docker exec -it kafka-kafka-1 /bin/kafka-console-consumer --topic test  --bootstrap-server kafka:19092 --from-beginning
```

You can type `Ctrl+C` to leave.


## (Optional) Step 6: Create a cluster
**Creating a cluster of two or more nodes requires a lot of resources, it may not run on your computer.**

For this you can use the following docker-compose or do `cp docker-compose-cluster.yml docker-compose.yml` (if you have cloned the git repo) or You can find an example in [docker-compose-cluster.yml](docker-compose-cluster.yml):

```yml
version: '3'

networks:
  tutorial:
    name: tutorial

services:
  zookeeper:
    image: zookeeper
    networks:
      - tutorial
    ports:
      - target: 2181
        published: 2181
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ALLOW_ANONYMOUS_LOGIN: "yes"

  kafka1:
    image: confluentinc/cp-kafka
    depends_on:
      - zookeeper
    networks:
      - tutorial
    ports:
      - "9092:9092"
      - "19092:19092"
    environment:
      KAFKA_BROKER_ID: 1
      ALLOW_PLAINTEXT_LISTENER: "yes"
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,HOST:PLAINTEXT
      KAFKA_LISTENERS: INTERNAL://0.0.0.0:19092,HOST://0.0.0.0:9092
      KAFKA_ADVERTISED_LISTENERS: HOST://localhost:9092,INTERNAL://kafka1:19092
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  kafka2:
    image: confluentinc/cp-kafka
    depends_on:
      - zookeeper
      - kafka1
    networks:
      - tutorial
    ports:
      - "9292:9292"
      - "29092:29092"
    environment:
      KAFKA_BROKER_ID: 2
      ALLOW_PLAINTEXT_LISTENER: "yes"
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,HOST:PLAINTEXT
      KAFKA_LISTENERS: INTERNAL://0.0.0.0:29092,HOST://0.0.0.0:9292
      KAFKA_ADVERTISED_LISTENERS: HOST://localhost:9292,INTERNAL://kafka1:29092
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

Once the instances are running, you can send messages and consume messages like before:

```docker
docker exec -it kafka-kafka1-1 /bin/kafka-topics --create --replication-factor 1 --partitions 1 --topic test --bootstrap-server kafka1:19092

docker exec -it kafka-kafka1-1 /bin/kafka-console-producer --topic test --bootstrap-server kafka1:19092

docker exec -it kafka-kafka2-1 /bin/kafka-console-consumer --topic test  --bootstrap-server kafka2:29092 --from-beginning
```


## Step 7: Playground

### Using Python with Kafka
To use the Python library we need to have librdkafka wheel installed. Some instructions on how to install it: https://github.com/confluentinc/librdkafka

For Windows users, installing librdkafka may be challeging, thefore, you can use devcontainers in VSC.

Hence, for the rest of this part we are going to use VSC and developer containers. The Devcontainer will not only make it easier to install librdkafka, but also similate the connection to Kafka from outside.

You need to make sure that you have the VSC extension Dev Containers installed: https://code.visualstudio.com/docs/devcontainers/tutorial#_install-the-extension

Once you have installed the extension, open the Command Palete of VSC (press F1) and type `Dev Containers: Open Folder in Container...` and then open the kafka folder. 

Once the devcontainer initialise, you need to install the python library `confluent-kafka` (from the terminal of VSC. If it does not show, in the top of the GUI, click the `...` and select Terminal > New Terminal)
```sh
pip install confluent-kafka
```
Let's produce some topics:

```sh
python producer.py kafka:19092 test
```

Finish the code with CTRL+C or CMD+C and consume the messages:

```sh
python consumer.py kafka:19092 group-test test
```

In the kafka directory you will find the `consumer.py` and `producer.py` to explore the code.


### Using Kafka REST
Kafka rest image is larger than 1.7GB, so it may not work on your computer. In case you want yo experiment, you can use the following docker-compose. You can find an example in [docker-compose-rest.yml](docker-compose-rest.yml) or do `cp docker-compose-rest.yml docker-compose.yml` (if you have cloned the git repo):

```yml
version: '3'

networks:
  tutorial:
    name: tutorial

services:
  zookeeper:
    image: zookeeper
    networks:
      - tutorial
    ports:
      - target: 2181
        published: 2181
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ALLOW_ANONYMOUS_LOGIN: "yes"

  kafka:
    image: confluentinc/cp-kafka
    depends_on:
      - zookeeper
    networks:
      - tutorial
    ports:
      - "9092:9092"
      - "19092:19092"
    environment:
      KAFKA_BROKER_ID: 1
      ALLOW_PLAINTEXT_LISTENER: "yes"
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,HOST:PLAINTEXT
      KAFKA_LISTENERS: INTERNAL://0.0.0.0:19092,HOST://0.0.0.0:9092
      KAFKA_ADVERTISED_LISTENERS: HOST://localhost:9092,INTERNAL://kafka:19092
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  rest-proxy:
    image: confluentinc/cp-kafka-rest
    depends_on:
      - kafka
    networks:
      - tutorial
    ports:
      - 8082:8082
    environment:
      KAFKA_REST_HOST_NAME: rest-proxy
      KAFKA_REST_BOOTSTRAP_SERVERS: 'kafka:19092'
      KAFKA_REST_LISTENERS: "http://0.0.0.0:8082"
```

Wait until the service is up and accepting requests. Then, you will be able to interact. To create a topic, you can send your first message.

```sh
curl -X POST \
     -H "Content-Type: application/vnd.kafka.json.v2+json" \
     -H "Accept: application/vnd.kafka.v2+json" \
     --data '{"records":[{"key":"jsmith","value":"alarm clock"},{"key":"htanaka","value":"batteries"},{"key":"awalther","value":"bookshelves"}]}' \
     "http://localhost:8082/topics/purchases"
```

The response should be similar to:

```sh
{"offsets":[{"partition":0,"offset":0,"error_code":null,"error":null},{"partition":0,"offset":1,"error_code":null,"error":null},{"partition":0,"offset":2,"error_code":null,"error":null}],"key_schema_id":null,"value_schema_id":null}  
```

To consume the messages, you need to create a consumer:

```sh
curl -X POST \
     -H "Content-Type: application/vnd.kafka.v2+json" \
     --data '{"name": "ci1", "format": "json", "auto.offset.reset": "earliest"}' \
     http://localhost:8082/consumers/cg1
```

Then, you need to subscrive the consumer to the topic:

```sh
curl -X POST \
     -H "Content-Type: application/vnd.kafka.v2+json" \
     --data '{"topics":["purchases"]}' \
     http://localhost:8082/consumers/cg1/instances/ci1/subscription 
```

To start consuming the data you need to execute the following (you only execute it twice on the first time):

```sh
curl -X GET \
     -H "Accept: application/vnd.kafka.json.v2+json" \
     http://localhost:8082/consumers/cg1/instances/ci1/records 

sleep 10

curl -X GET \
     -H "Accept: application/vnd.kafka.json.v2+json" \
     http://localhost:8082/consumers/cg1/instances/ci1/records 
```

Finaly, when you finish consuming messages, remever to close the consumer:

```sh
curl -X DELETE \
     -H "Content-Type: application/vnd.kafka.v2+json" \
     http://localhost:8082/consumers/cg1/instances/ci1 
```

## Trobleshooting
### Checking the logs
To check the logs of a container an see what is happending or the errors use:
```sh
docker compose logs <container-name>
```

### Default docker IP address
In windows you can check the address of your docker engine by opening Docker Desktop and going to settings. There go to Resources > Network

## Addition resources
This resources can help you to expand your knowledge on Apache Kafka:
- https://kafka.apache.org/documentation.html

An sql-like database build on top of Apache Kafka:
- KsqlDB: https://ksqldb.io/