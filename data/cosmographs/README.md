# Cosmograph seed data

Machine-readable catalog of cosmographs for ingestion into Kosmographica.

| File | Rows | Spec |
|---|---|---|
| [`catalog.json`](./catalog.json) | 162 | Canonical seed (built from CSV + expansions) |
| [`catalog.csv`](./catalog.csv) | 74 | Original Indo-European/Western-heavy subset |
| [`build_catalog.py`](./build_catalog.py) | — | Regenerates `catalog.json` from CSV + `NEW_RECORDS` |

Intended `Entity` shape: `type: Cosmograph`, `module: philosophy-science` (or religion-mythology for
mythic/shamanic entries), `data` fields mapped from catalog columns.

**Ingest:**

```bash
cd engine && uv run kge seed cosmograph ../data/cosmographs/catalog.json
```

**Images (Wikimedia Commons):**

```bash
python3 data/cosmographs/fetch_images.py
cd engine && uv run kge seed cosmograph ../data/cosmographs/catalog.json
```

Re-seeding merges new `data` fields (including image URLs) into existing cosmograph entities.
