# Image Scanning

|||objectives
After this lecture, you should be able to answer the following:
- How do you scan an image for vulnerabilities?
- How do you scan a running container?
- What tools are available for scanning?
- What do you do when you find a vulnerability?
|||

In the last lecture, we looked inside images and saw how secrets can leak through layers. In this lecture, we are going to scan images for known vulnerabilities and learn what to do about them.

### Scanning Tools

There are three popular tools for scanning container images:

**Docker Scout** (built into Docker)
```bash
# Quick scan
sudo docker scout cves python:3.12-slim
```

**Trivy** (by Aqua Security, open source)
```bash
# Install (see https://trivy.dev/latest/getting-started/installation/)
sudo apt-get install wget apt-transport-https gnupg
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install -y trivy
# Scan an image
trivy image python:3.12-slim
# Scan and only show high/critical
trivy image --severity HIGH,CRITICAL python:3.12-slim
```

### Let's Scan Some Images

Try scanning images you already know:

```bash
trivy image python:3.12
trivy image python:3.12-slim
trivy image python:3.12-alpine
trivy image mywebapp
```

### Scanning a Project Folder

Trivy can also scan a whole project folder, including your Dockerfile, for misconfigurations and secrets. Let's scan the web app from last lecture:

```bash
trivy fs --scanners vuln,secret,misconfig myproject/
```

### Why Running as Root is Dangerous

By default, a container runs as the root user. This is convenient, but it is a security problem.

If an attacker breaks into your application (through a bug, a vulnerable library, anything), they get whatever privileges the container process has. If that process is root, the attacker is now root inside the container. From there they can install tools, read every file, and have a much easier time trying to break out of the container onto the host.

### Fixing It with the USER Instruction

The `USER` instruction tells Docker which user to run as. Add a non-root user in your Dockerfile and switch to it before the app runs:

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY app.js .

# Create a non-root user and switch to it
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 3000
CMD ["node", "app.js"]
```

Now the container runs as `appuser` instead of root. Rebuild and scan again, and the HIGH finding disappears.

### Scanning Running Containers

```bash
# Copy Trivy into the container and scan from inside
sudo docker cp $(which trivy) mycontainer:/usr/local/bin/trivy
sudo docker exec mycontainer trivy fs /
```

### Automating Scans

Scanning manually is fine for learning. In the real world, scanning happens automatically:

- **At build time:** scan the image in your CI/CD pipeline before it gets deployed. If critical vulnerabilities are found, the build fails.
- **In a registry:** Docker Hub, GitHub Container Registry, and others can scan images when you push them.
- **On a schedule:** images that were clean last week might have new CVEs this week. Regular rescans catch them.

```bash
# Example: fail a CI pipeline if critical CVEs are found
trivy image --exit-code 1 --severity CRITICAL mywebapp
```

The `--exit-code 1` flag makes Trivy return a non-zero exit code if it finds critical issues. Your CI pipeline treats this as a failed build.

|||quiz
- Why does a smaller base image improve security?
- What is the difference between scanning an image and scanning a running container?
- What does `--exit-code 1` do when used with Trivy?
- Why is running a container as root dangerous, and how do you fix it?
|||

<div style="text-align: center; font-size: 0.8em; color: gray; margin-top: 50px;">Maysara Alhindi -- 2026</div>