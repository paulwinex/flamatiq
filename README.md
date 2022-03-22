# Flamatiq

#### _(Flask + dramatiq)_

Flask application example with background task queue based on [dramatiq](https://dramatiq.io/).

Features:

- Simple tasks
- Task with result
- Abortable task with [dramatiq_abort](https://github.com/Flared/dramatiq-abort)
- Shelled periodic task with [periodiq](https://github.com/gimi-org/periodiq)
- Dockerized and "Composed"

### Usage 

_You need to install docker and docker-compose before start_

```bash
sudo apt-get install -y docker.io
sudo pip3 install docker-compose
```

Build the image

```bash
make build
```

Start containers

```bash
make up
```

And go to http://localhost:8095/

To stop stack press Ctrl+C
