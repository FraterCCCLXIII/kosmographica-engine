# Database snapshots

Logical backups of the local Kosmographica Postgres corpus (`kosmographica` on port **5459**).

## Latest

| File | Created (UTC) | Size | Rows (approx.) |
|------|---------------|------|----------------|
| `kosmographica-20260604T234851Z.dump` | 2026-06-04T23:48:51Z | 1.1 MB | 4376 entities, 3989 relationships, 6985 claims |

Format: PostgreSQL custom archive (`pg_dump -Fc`). Restore with `pg_restore`, not plain `psql`.

## Restore (Docker dev DB)

```bash
cd engine
docker compose up -d db
# empty target DB first if replacing in place:
docker exec -i engine-db-1 psql -U kosmo -d postgres -c \
  "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'kosmographica' AND pid <> pg_backend_pid();"
docker exec -i engine-db-1 psql -U kosmo -d postgres -c "DROP DATABASE IF EXISTS kosmographica;"
docker exec -i engine-db-1 psql -U kosmo -d postgres -c "CREATE DATABASE kosmographica OWNER kosmo;"
docker exec -i engine-db-1 pg_restore -U kosmo -d kosmographica --no-owner --no-acl \
  < data/snapshots/kosmographica-20260604T234851Z.dump
```

Run `pg_restore` from the repo root, or copy the `.dump` file into the container and restore there.

## Create a new snapshot

```bash
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
docker exec engine-db-1 pg_dump -U kosmo -d kosmographica --no-owner --no-acl -Fc \
  > "data/snapshots/kosmographica-${STAMP}.dump"
```
