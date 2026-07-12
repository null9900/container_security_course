# Denial of Service & Resource Limits

|||objectives
After this lecture, you should be able to answer the following:
- How can a single container take down a whole host?
- What does a denial of service look like inside a container?
- How do you set CPU and memory limits?
- How do limits protect the host and the other containers?
|||

Back in the first lecture, we imagined renting out a powerful server, and one user's app eating all the RAM and crashing everyone else. In this lecture, we are going to make that happen on purpose, and then prevent it.

By default, a container can use as much CPU and memory as it wants. There is no limit. All containers share the host's resources, and nothing stops one container from taking everything.

### Examples of DDoS that brings that host down

```bash
sudo docker run -it python:3.12-slim python3 -c "x = []
while True:
    x.append(' ' * 10**7)"
```

```bash
sudo docker run -it alpine sh -c "while true; do :; done"
```

```bash
sudo docker run -it alpine sh -c ":(){ :|:& };:"
```

### Setting Memory Limits

You limit memory with the `-m` (or `--memory`) flag:

```bash
sudo docker run -m 256m -it python:3.12-slim sh
```

### Setting CPU Limits

You limit CPU with the `--cpus` flag:

```bash
sudo docker run --cpus 0.5 -it alpine sh -c "while true; do :; done"
```

`--cpus 0.5` means the container can use at most half of one CPU core. The CPU DDoS still runs, but it can no longer saturate the machine. Other containers keep getting their share.

### Limiting Processes

To stop fork DDoSs, limit the number of processes with `--pids-limit`:

```bash
sudo docker run --pids-limit 100 -it alpine sh
```
Now the container can create at most 100 processes. A fork DDoS hits the limit and stops, instead of taking down the host.

### Limits in Docker Compose

In a Compose file, you set the same limits under each service:

```yaml
services:
  app:
    build: .
    mem_limit: 256m
    cpus: 0.5
    pids_limit: 100
```

### Checking Resource Usage

To see what your containers are actually using in real time:

```bash
sudo docker stats
```

|||quiz
- What is a denial of service in the context of containers?
- How do you limit a container's memory, and what happens when it hits the limit?
- Which command shows live resource usage for running containers?
|||

<div style="text-align: center; font-size: 0.8em; color: gray; margin-top: 50px;">Maysara Alhindi -- 2026</div>