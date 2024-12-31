# Phidata, Postgres, and pgvector Setup

This guide outlines the steps to set up and use Phidata with Postgres and pgvector.

### Step 1: Start a Postgres Database with pgvector

Run the following Docker command to start a Postgres database with the `pgvector` extension:

```bash
docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgvolume:/var/lib/postgresql/data \
  -p 5532:5432 \
  --name pgvector \
  phidata/pgvector:16
```

### Step 2: Verify the Setup

To confirm that the container is running:

```bash
docker ps 
```

### Step 3: Access the Database

You can connect to the database using any Postgres client or CLI tool. For example, using `psql`:

```bash
psql -h localhost -p 5532 -U ai -d ai
```

When prompted, enter the password: `ai`.

