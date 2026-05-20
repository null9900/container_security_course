# Running Multi-Container Applications

|||objectives
After this lecture, you should be able to answer the following:
- What is Docker Compose and why do we need it?
- How do you write a docker-compose.yml file?
- How do you start, stop, and manage multi-container applications?
|||

So far we have been running one container at a time. In the real world, applications are rarely just one container. A web app might need a web server, a database, and a cache. Running each one manually with `docker run` and connecting them together gets messy fast.

Docker Compose solves this. You describe all your containers in one file, and start everything with one command.

### Installing Docker Compose

Docker Compose comes pre-installed with Docker Desktop. On Linux, check if you have it:

```bash
docker compose version
```

If not, install it:

```bash
sudo apt install docker-compose-plugin
```

### Your First Compose File

Create a file called `docker-compose.yml`:

```yaml
services:
  web:
    image: alpine
    command: echo "hello from compose"
```

Run it:

```bash
sudo docker compose up
```

You should see `hello from compose` printed in your terminal. Press `Ctrl+C` to stop.

To run in the background:

```bash
sudo docker compose up -d
```

### The docker-compose.yml Structure

A compose file defines **services**. Each service becomes a container.

```yaml
services:
  web:
    image: alpine
  db:
    image: postgres
```

This creates two containers: one running Alpine, one running PostgreSQL. Docker Compose handles naming, networking, and startup for you.

### Building from a Dockerfile

Remember the Python web app from last lecture? We can run it with Compose instead of typing a long `docker run` command.

Put the Dockerfile, `app.py`, and `index.html` from last lecture in a folder, then create a `docker-compose.yml`:

```yaml
services:
  web:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
```

That is it. One file replaces this entire command:

```bash
sudo docker run -d --name webapp -p 8080:8080 -v $(pwd)/data:/app/data mywebapp
```

Run it:

```bash
sudo docker compose up -d
```

Open `http://localhost:8080`, refresh a few times, and check the `./data/access.log` file on your host. Same result as last lecture, but now the configuration is saved in a file instead of a command you have to remember.

### depends_on

Sometimes one container needs another to be running first. A web app should not start before its database is ready. `depends_on` controls the startup order:

```yaml
services:
  web:
    build: .
    depends_on:
      - db
  db:
    image: postgres
```

### Environment Variables

You can pass environment variables to containers:

```yaml
services:
  db:
    image: postgres
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
```

Docker Compose will start `db` first, then `web`.

### Environment Variables: Do Not Hardcode Secrets

This works but it is a bad idea:

```yaml
services:
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: secret123
```

Anyone who sees the compose file sees the password. Instead, use a `.env` file.

Create a `.env` file next to your `docker-compose.yml`:

```
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret123
POSTGRES_DB=myapp
DB_PORT=5432
```

Then reference the variables in the compose file with `${}`:

```yaml
services:
  db:
    image: postgres
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
```

Docker Compose reads the `.env` file automatically. Add `.env` to your `.gitignore` so secrets never end up in version control.

### Networking

Docker Compose creates a network for all services automatically. Containers can reach each other **by service name**. If you have a service called `db`, other containers can connect to it using `db` as the hostname. No IP addresses, no manual network setup.


### Managing Compose Applications

```bash
# Start everything in the background
sudo docker compose up -d

# See running containers
sudo docker compose ps

# View logs from all containers
sudo docker compose logs

# View logs from one service
sudo docker compose logs web

# Stop everything
sudo docker compose stop

# Stop and remove everything (containers, networks)
sudo docker compose down
```

### A Real Example: Node.js + PostgreSQL + Adminer

Three services working together:
- **app** - A Node.js web server that writes to the database
- **db** - PostgreSQL database
- **adminer** - A web UI to browse the database

Create the project folder:

```bash
mkdir myproject && cd myproject
```

Create `app.js`:

```javascript
const http = require("http");
const { Client } = require("pg");

async function start() {
  let client;

  // Wait for database to be ready
  while (true) {
    try {
      client = new Client({
        host: "db",
        user: process.env.POSTGRES_USER,
        password: process.env.POSTGRES_PASSWORD,
        database: process.env.POSTGRES_DB,
      });
      await client.connect();
      console.log("Connected to database");
      break;
    } catch (err) {
      console.log("Waiting for database...");
      await new Promise((r) => setTimeout(r, 2000));
    }
  }

  await client.query(`
    CREATE TABLE IF NOT EXISTS visits (
      id SERIAL PRIMARY KEY,
      timestamp TIMESTAMP DEFAULT NOW()
    )
  `);

  const server = http.createServer(async (req, res) => {
    if (req.url === "/") {
      await client.query("INSERT INTO visits DEFAULT VALUES");
      const result = await client.query("SELECT COUNT(*) FROM visits");
      const count = result.rows[0].count;
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end(`<h1>Visits: ${count}</h1>`);
    }
  });

  server.listen(3000, () => console.log("Server running on port 3000"));
}

start();
```

Create `package.json`:

```json
{
  "name": "myapp",
  "version": "1.0.0",
  "dependencies": {
    "pg": "^8.11.0"
  }
}
```

Create `Dockerfile`:

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY app.js .
EXPOSE 3000
CMD ["node", "app.js"]
```

Create `.env`:

```
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret123
POSTGRES_DB=myapp
```

Create `docker-compose.yml`:

```yaml
services:
  app:
    build: .
    ports:
      - 3000:3000
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}

  adminer:
    image: adminer
    ports:
      - 8081:8080
    depends_on:
      - db
```

A few things to notice:
- The `app` service connects to `host: "db"`. That is the service name. Compose handles the DNS.
- Both `app` and `db` read from the same `.env` file. The password is defined once.
- `depends_on` makes sure `db` starts before `app` and `adminer`.

### Putting It All Together

```bash
# 1. Start everything
sudo docker compose up -d

# 2. Check all three containers are running
sudo docker compose ps

# 3. Open http://localhost:3000 and refresh a few times

# 4. Open http://localhost:8081 to see the database dashboard
#    System: PostgreSQL
#    Server: db
#    Username: admin
#    Password: secret123
#    Database: myapp
#    Look at the "visits" table

# 5. Check the logs
sudo docker compose logs

# 6. Tear it all down
sudo docker compose down
```

### docker run vs docker compose

| | `docker run` | `docker compose` |
|---|---|---|
| Containers | One at a time | Multiple at once |
| Configuration | Flags on the command line | Written in a YAML file |
| Networking | Manual | Automatic between services |
| Reproducibility | Have to remember the command | Just run `docker compose up` |

|||quiz
- What problem does Docker Compose solve?
- How do containers in a compose file communicate with each other?
- What does `docker compose down` do? How is it different from `docker compose stop`?
- Why should you use a `.env` file instead of hardcoding secrets in the compose file?
- Build the Node.js + PostgreSQL + Adminer app from this lecture. Verify the web app works, browse the database through Adminer, then tear it all down.
|||

<div style="text-align: center; font-size: 0.8em; color: gray; margin-top: 50px;">Maysara Alhindi -- 2026</div>