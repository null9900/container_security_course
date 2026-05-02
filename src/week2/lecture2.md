# Running Your First Container

|||objectives
After this lecture, you should be able to answer the following:
- How do you install Docker on a Linux machine?
- How do you use the Docker CLI to pull and run images?
- How do you manage container lifecycles using run, stop, ps, and rm?
|||

In the last lecture, we talked about **what** containers are and **why** they matter. In this lecture, we are going to learn how to use them.

### Installing Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Verify that Docker is installed and running:

```bash
sudo docker --version
```

### Image vs. Container

- Image: A read-only template. Like a recipe or a blueprint.
- Container: A running instance of an image. Like a dish made from that recipe.

You **pull** images. You **run** containers.

You can download images from [Docker Hub](https://hub.docker.com), which is like an app store for container images.

![Containers-old](https://docs.docker.com/get-started/images/docker-architecture.webp)


```bash
# This downloads the Alpine Linux image from Docker Hub.
sudo docker pull alpine
```

```bash
# This shows all the images you have downloaded on your machine.
sudo docker image ls
```

### Running Your First Container

```bash
# This creates a container from the Alpine image. It runs and exits immediately because Alpine has nothing to do by default.
sudo docker run --name testalpine alpine
```

```bash
# The `-it` flags give you an **interactive terminal**. You are now inside the container. Type `exit` to leave.
sudo docker run -it --name testalpine alpine
```

```bash
# The `-d` flag runs the container **detached** (in the background). You get your terminal back.
sudo docker run -dit --name testalpine alpine

# To connect to it later:
sudo docker exec -it testalpine sh
```

```bash
# The `--rm` flag automatically deletes the container when you exit.
sudo docker run -it --rm alpine
```

### Listing Containers

Stopped containers do not disappear. They stay on your system until you explicitly remove them.

```bash
# Show running containers
sudo docker container ls
sudo docker ps
# Show ALL containers (including stopped ones)
sudo docker ps -a
```

### Managing Container Lifecycles

```bash
# Start a stopped container
sudo docker start testalpine
# Stop a running container
sudo docker stop testalpine
# Remove a stopped container permanently
sudo docker rm testalpine
```

### Exposing Ports

Some images run services that listen on a port. To access them from your browser, use the `-p` flag.

Format: `-p HOST_PORT:CONTAINER_PORT`

### Putting It All Together

Let's use everything we learned to run Excalidraw, a full collaborative whiteboard app, in one command.

```bash
# 1. Pull the image
sudo docker pull excalidraw/excalidraw
# 2. Run it in the background with a port mapping
sudo docker run -d --name drawing -p 3000:80 excalidraw/excalidraw
# 3. Open http://localhost:3000 in your browser
# 4. Check that the container is running
sudo docker ps
# 5. Go inside the container and look around
sudo docker exec -it drawing sh
exit
# 6. Stop the container
sudo docker stop drawing
# 7. Verify it stopped (notice the STATUS column)
sudo docker ps -a
# 8. Remove the container
sudo docker rm drawing
# 9. Verify it's gone
sudo docker ps -a
```

|||quiz
- What is the difference between a Docker image and a Docker container?
- What does the `-d` flag do in `docker run`?
- What does the `--rm` flag do?
- What does `-p 3000:80` mean?
- What is the difference between `docker stop` and `docker rm`?
- What is the difference between `docker run` and `docker start`?
- Run the excalidraw container, access it from your browser, then stop and remove it.
|||

<div style="text-align: center; font-size: 0.8em; color: gray; margin-top: 50px;">Maysara Alhindi -- 2026</div>