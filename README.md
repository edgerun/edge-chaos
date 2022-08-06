# Edge Chaos

This project's aim is to cause chaos in edge-cloud environments.

Users can start and stop programs that should disrupt co-located applications.
Currently the following features are implemented:

* CPU stress (using `stress-ng`)
* Network traffic shaping (using `tc`)

## Install

Run the following steps to install all dependencies:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## Build

We offer scripts to containerize the application for all common architectures (i.e., `amd64`, `arm32v7` and `arm64v8`):

    ./scripts/docker-build.sh $arch

## Release

    ./scripts/docker-release.sh $repository $version

The `version` argument is optional and defaults to `$(git rev-parse --short HEAD)`.

## Run

While it's main intended use case is to run in a container, you can also start it natively:

    python3 -u -m edgechaos.daemon.run

To start as a container run:

    docker run --network=host edgerun/edge-chaos:latest

Usage
=====

EdgeChaos runs as a daemon (native, in a container or in a Kubernetes Pod) and waits to receive commands.
Currently, commands are expected to arrive via Redis Pub/Sub or via AMQP (i.e., RabbitMQ).

Supported **interaction**:

* **Redis**: the daemon waits for messages published via the channel `edgechaos/$edgechaos_host`.
  Whereas `$edgechaos_host` is set as environment variable and defaults to the `HOSTNAME`.

The expected body is the same across the different interaction methods.
The daemon expects the message to be a JSON object, that has a `name`, `parameters` and `kind` key.
The `name` indicates the type of attack (i.e., `cpu`) and the `parameters` specify further information necessary for the
attack.
The `kind` specifies whether it's a `start` or `stop` event.
You can get a more detailed glimpse into the format by taking a look at the corresponding
dataclass [ChaosCommand](edgechaos/executor/api.py).

**Important:** The body must be always the same. Which means if you want to stop an attack, you have to send the same
body as before, except `kind` is set to `stop`.

To give an example, the following two JSON objects show how to start a CPU attack (using 1 core) and stop it.

Start the attack:

```json
{
  "name": "cpu",
  "parameters": {
    "cores": 1
  },
  "kind": "start"
}
```

And stop it:

```json
{
  "name": "cpu",
  "parameters": {
    "cores": 1
  },
  "kind": "stop"
}
```

Environment variables
=====================

| Name                     | Default     | Description |
|--------------------------|-------------|-------------|
| edgechaos_logging_level  | `INFO`      | Sets [logger level](https://docs.python.org/3/library/logging.html#levels) |
| edgechaos_redis_host     | `localhost` | Redis host |
| edgechaos_redis_port     | `6379`      | Redis port |
| edgechaos_redis_password | N/A         | Redis password |
| edgechaos_listener_type  | `redis`     | Listener type (currently supported: `redis`)
| edgechaos_client_type    | `redis`     | Client type (currently supported: `redis`)
| edgechaos_host           | $HOSTNAME   | Hostname, determines the channel the daemon listens to |