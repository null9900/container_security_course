# Dockerfiles: Building Your Own Images

|||objectives
After this lecture, you should be able to answer the following:
- What is a Dockerfile?
- How do you write a Dockerfile from scratch?
- How do you build an image from a Dockerfile?
- What are the most common Dockerfile instructions?
|||

So far we have been pulling images that other people made. In this lecture, we are going to build our own.

### What is a Dockerfile?

A Dockerfile is a text file that contains a list of instructions. Docker reads these instructions and builds an image from them, step by step.

Dockerfile -> custom image.

|||info
Dockerfiles are everywhere:

**Tesla** - [Fleet Telemetry](https://github.com/teslamotors/fleet-telemetry)

**NASA** - [Astrobee](https://github.com/nasa/astrobee)

**Microsoft** - [presidio](https://github.com/microsoft/presidio)

**Rapid7** - [Metasploit](https://github.com/rapid7/metasploit-framework/)
|||


### Your First Dockerfile

Create a file called `Dockerfile` (no extension):

```dockerfile
FROM alpine
CMD echo "hello from my first image"
```

### Building an Image

```bash
sudo docker build -t myfirstimage .
```

- `docker build` reads the Dockerfile and creates an image.
- `-t myfirstimage` gives the image a name (a tag).
- `.` tells Docker to look for the Dockerfile in the current directory.

Check your images:
```bash
sudo docker images
```

Now run it:
```bash
sudo docker run myfirstimage
```
You should see `hello from my first image` printed in your terminal.

### Dockerfile Instructions

#### FROM

Every Dockerfile starts with `FROM`. It sets the base image you are building on top of.

```dockerfile
FROM alpine
```

```dockerfile
FROM python:3.12-slim
```

You always build on top of something. You do not start from zero.

#### RUN

`RUN` executes a command during the build process. Use it to install packages, create directories, or set things up.

```dockerfile
FROM alpine
RUN apk add curl
```

Each `RUN` instruction creates a new **layer** in the image. More on layers later.

#### WORKDIR

`WORKDIR` sets the working directory inside the image. Every instruction after it runs from that directory.

```dockerfile
WORKDIR /app
```

If the directory does not exist, Docker creates it.

#### COPY

`COPY` takes a file from your machine and puts it inside the image.

```dockerfile
COPY index.html /app
```

The first argument is the file on your machine. The second is where it goes inside the image.

#### CMD

`CMD` defines the default command that runs when a container starts.

```dockerfile
CMD ["python", "app.py"]
```

A Dockerfile should have one `CMD`. If you write multiple, only the last one counts.

#### ENTRYPOINT 

`ENTRYPOINT` is similar to CMD, but it cannot be overridden when running the container. Anything you pass at runtime gets appended as arguments to the ENTRYPOINT command. 

#### VOLUME

`VOLUME` creates a mount point for external storage. When a container is removed, everything inside it is lost. Volumes let you keep data alive beyond the container's lifecycle.

```dockerfile
VOLUME /app/data
```

This tells Docker that `/app/data` should be stored outside the container.

When running the container, we can specifiy where exactly that volume maps in the host using `-v` flag.
```bash
sudo docker run -v $(pwd)/mydata:/app/data myimage
```

#### EXPOSE

`EXPOSE` documents which port the container will listen on. It does not actually open the port. You still need `-p` when you run the container.

```dockerfile
EXPOSE 8080
```

### A Real Example: Python App

Create a simple Python script called `app.py`:

```python
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

class LoggingHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        with open("/app/data/access.log", "a") as f:
            f.write(f"{datetime.now()} - {self.path}\n")
        super().do_GET()

print("Server running on port 8080")
HTTPServer(("0.0.0.0", 8080), LoggingHandler).serve_forever()```

Create an `index.html`:
```

```html
<h1>Hello from my container!</h1>
```

Now write the Dockerfile:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN echo "built on $(date)" > /build-info.txt
COPY index.html /app
COPY app.py /app
CMD ["python", "app.py"]
VOLUME /app/data
EXPOSE 8080```
```

Build and run:

```bash
# Build the image
sudo docker build -t mywebapp .
# Run it
sudo docker run --rm --name webapp -p 8080:8080 -v $(pwd)/logs:/app/data mywebapp
# Check the container
sudo docker ps
```

Open `http://localhost:8080` in your browser. That page is being served from your own custom image.

|||info
Every instruction in a Dockerfile creates a layer. Layers are cached, so if you change line 5 in your Dockerfile, Docker reuses the cached layers for lines 1 through 4 and only rebuilds from line 5 onward.

This is why you should put things that change often (like copying your code) at the bottom, and things that rarely change (like installing packages) at the top.
|||

|||info
Remember Excalidraw from last lecture? That whiteboard app you launched with one command? Go look at its Dockerfile on GitHub: [github.com/excalidraw/excalidraw/blob/master/Dockerfile](https://github.com/excalidraw/excalidraw/blob/master/Dockerfile). You will see the same instructions we learned today: `FROM`, `COPY`, `RUN`, `EXPOSE`.
|||

|||quiz
- What is the purpose of a Dockerfile?
- What does the `FROM` instruction do?
- What is the difference between `RUN` and `CMD`?
- What does `COPY` do?
- Does `EXPOSE` actually open a port?
- Why does the order of instructions in a Dockerfile matter?
- Build the Python web app from this lecture, run it, verify it works in your browser, then stop and remove it.
|||

<div style="text-align: center; font-size: 0.8em; color: gray; margin-top: 50px;">Maysara Alhindi -- 2026</div>