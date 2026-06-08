#!/usr/bin/env python3
"""Fetch Wikimedia Commons thumbnails for cosmograph catalog entries."""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CATALOG = Path(__file__).resolve().parent / "catalog.json"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
WIKIDATA_API = "https://www.wikidata.org/w/api.php"
USER_AGENT = "KosmographicaBot/1.0 (cosmograph catalog; contact: kosmographica)"

# Hand-tuned queries where label-only search is weak.
SEARCH_OVERRIDES: dict[str, str] = {
    "AQAL": "Ken Wilber integral theory diagram",
    "Pañca-Kośa": "Pancha Kosha diagram",
    "Sāṃkhya Tattvas": "Samkhya tattvas chart",
    "Abhidharma Mind Map": "Abhidharma dharmas chart",
    "Islamic Falasifa Cosmos": "Ibn Sina cosmology",
    "Illuminationist Cosmos": "Suhrawardi illumination philosophy",
    "Akbarian Cosmos": "Ibn Arabi cosmology",
    "Mappa Mundi": "Hereford Mappa Mundi",
    "Dantean Cosmos": "Divine Comedy cosmology Gustave Dore",
    "Fludd Cosmos": "Robert Fludd macrocosm",
    "Kircher Cosmos": "Athanasius Kircher cosmology",
    "Copernican Cosmos": "Copernican heliocentric diagram",
    "Keplerian Cosmos": "Kepler Mysterium Cosmographicum",
    "Newtonian Universe": "Newton Principia cosmos",
    "Linnaean Taxonomy": "Linnaeus Systema Naturae tree",
    "Darwinian Tree": "Darwin tree of life",
    "Freud Topography": "Freud psychic apparatus diagram",
    "Jungian Psyche": "Jung mandala self",
    "Relativistic Cosmos": "Einstein general relativity spacetime",
    "Big Bang Universe": "Big Bang timeline diagram",
    "Inflationary Universe": "cosmic inflation diagram",
    "Cosmic Web": "cosmic web large scale structure",
    "Spiral Dynamics": "Spiral Dynamics Graves",
    "General Systems Theory": "Bertalanffy general systems",
    "Cybernetics": "Norbert Wiener cybernetics",
    "Autopoiesis": "Maturana Varela autopoiesis",
    "Gaia Theory": "Gaia hypothesis Earth",
    "Network Science": "Barabasi network science",
    "Semantic Web": "semantic web diagram",
    "Embedding Space Cosmology": "word2vec vector space",
    "Foundation Model World Models": "transformer architecture diagram",
    "Agentic Cosmology": "multi-agent AI diagram",
    "Integrated Information Theory": "integrated information theory phi",
    "Free Energy Principle": "Karl Friston free energy",
    "Constructor Theory": "David Deutsch constructor theory",
    "Kongo Cosmogram": "Kongo cosmogram dikenga",
    "Huayan Indra's Net": "Indra's net Avatamsaka",
    "Huayan Cosmos": "Huayan Buddhism cosmology",
    "Kalachakra Mandala": "Kalachakra mandala",
    "Popol Vuh Cosmos": "Popol Vuh Maya creation",
    "Maya World Tree": "Maya world tree ceiba",
    "Inca Three Worlds": "Inca cosmology three worlds",
    "Yggdrasil": "Yggdrasil world tree Norse",
    "Whitehead Process Cosmos": "Alfred North Whitehead process philosophy",
    "Teilhard Noosphere": "Teilhard de Chardin noosphere",
    "Gebser Structures of Consciousness": "Jean Gebser consciousness structures",
    "Sefer Yetzirah Cosmos": "Tree of Life Kabbalah",
    "Golden Dawn Tree": "Kabbalah Tree of Life Golden Dawn",
    "Actor-Network Theory": "Bruno Latour actor network",
    "Planetary Boundaries": "planetary boundaries Stockholm Resilience",
    "Deep Ecology": "deep ecology Arne Naess",
    "Cellular Automata Universe": "Stephen Wolfram cellular automata",
    "Digital Physics": "Konrad Zuse digital physics",
    "Connectionist Networks": "neural network diagram PDP",
    "Transformer Latent Spaces": "transformer attention diagram",
    "World Models": "AI world model architecture",
    "Agentic Societies": "multi-agent LLM society",
    "AI-generated Knowledge Graphs": "knowledge graph AI extraction",
    "Knowledge Graphs": "RDF knowledge graph diagram",
    "Indra's Net": "Indra's net Buddhism",
    "Cook-Greuter Ego Development": "ego development stages Cook Greuter",
    "Yin-Yang Cosmology": "Yin Yang taijitu",
    "Five Phases Cosmology": "Wu Xing five phases",
    "Daoist Internal Cosmography": "Daoist inner landscape microcosm",
    "Tibetan Bardo Cosmology": "Bardo Thodol mandala",
    "Tibetan Medical Cosmology": "Tibetan medicine body channels",
    "Neo-Confucian Li/Qi Cosmos": "Neo-Confucian li qi diagram",
    "Navajo Emergence Cosmology": "Navajo emergence cosmology",
    "Lakota Sacred Hoop": "Lakota medicine wheel sacred hoop",
    "Hopi World Ages": "Hopi world ages cosmology",
    "Ojibwe Midewiwin Cosmos": "Midewiwin birchbark scroll",
    "Aztec 13 Heavens": "Aztec cosmology thirteen heavens",
    "Aztec 9 Underworlds": "Aztec underworld Mictlan",
    "Teotihuacan Cosmic Plan": "Teotihuacan Avenue of the Dead",
    "Andean Chakana": "Chakana Inca cross",
    "Amazonian Shamanic Cosmos": "Amazon shamanic cosmology ayahuasca",
    "Dogon Universe": "Dogon cosmology Sirius",
    "Ancient Nubian Cosmos": "Kushite Nubian pyramid cosmology",
    "Mongolian Shamanic Cosmos": "Mongolian shaman cosmology",
    "Finno-Ugric World Tree": "Finno-Ugric world tree",
    "Rosicrucian Universe": "Rosicrucian emblem",
    "Thelemic Cosmology": "Aleister Crowley Tree of Life",
    "Bergson Evolutionary Cosmos": "Henri Bergson creative evolution",
    "Earth System Science": "Earth system science diagram",
    "Computational Universe": "digital physics universe",
    "Connectomics": "human connectome brain map",
    "Symbolic Knowledge Graphs": "semantic network AI Cyc",
    "Mithraic Cosmos": "Mithraic tauroctony cosmology",
    "Manichaean Cosmos": "Manichaean cosmology diagram",
    "Bundahishn Universe": "Zoroastrian cosmology Bundahishn",
    "Mandaean Cosmos": "Mandaean cosmology",
    "Chaldean Cosmology": "Babylonian planetary spheres",
    "Harranian Sabian Cosmos": "Harran Sabian astronomy",
    "Ismaili Emanation Cosmology": "Ismaili cosmology emanation",
    "Illuminationist Light Cosmos": "Suhrawardi light philosophy",
    "Dzogchen Ground-Path-Fruit": "Dzogchen rigpa diagram",
    "Mahamudra Cosmology": "Mahamudra Tibetan Buddhism",
    "Tiantai Three Truths": "Tiantai Buddhism three truths",
    "Tendai Cosmos": "Tendai Buddhism Japan",
    "Shingon Mandala Universe": "Shingon mandala Womb Realm",
    "Korean Seon Cosmology": "Korean Seon Buddhism",
    "Haudenosaunee Sky World": "Haudenosaunee creation sky world",
    "Inuit Layered Cosmos": "Inuit cosmology layers",
    "Mixtec Cosmology": "Mixtec codex cosmology",
    "Toltec Cosmology": "Toltec cosmology",
    "Muisca Cosmos": "Muisca El Dorado cosmology",
    "Tupi-Guarani Cosmos": "Tupi Guarani Land without Evil",
    "Mapuche Cosmos": "Mapuche cosmology nuke mapu",
    "Yoruba Cosmos": "Yoruba orisha cosmology",
    "Akan Cosmos": "Akan cosmology Ghana",
    "Dinka Cosmos": "Dinka Nilotic cosmology",
    "Zulu Cosmos": "Zulu cosmology ancestors",
    "Berber Cosmology": "Amazigh Berber cosmology",
    "Nart Cosmos": "Nart sagas Caucasus",
    "Sámi Cosmos": "Sami noaidi drum cosmology",
    "Turkic Sky Cosmos": "Tengrism Turkic sky cosmology",
    "Jacob Boehme Cosmos": "Jacob Boehme theosophy diagram",
    "Swedenborg Cosmos": "Emanuel Swedenborg heaven hell",
    "Megalithic Sky Map": "Stonehenge astronomical alignment",
    "Three Worlds": "shamanic three worlds cosmology",
    "World Tree": "world tree axis mundi",
    "Sumerian Cosmos": "Sumerian cosmology Enuma Elish",
    "Babylonian World Map": "Babylonian world map BM 92687",
    "Egyptian Cosmos": "ancient Egyptian cosmology Nut Geb",
    "Duat Map": "Egyptian Duat Amduat",
    "Zoroastrian Cosmos": "Zoroastrian cosmology Faravahar",
    "Vedic Three Worlds": "Vedic trailokya three worlds",
    "Puranic Universe": "Puranic cosmology Mount Meru",
    "Jain Lokapurusha": "Jain lokapurusha cosmology",
    "Buddhist Meru Cosmos": "Buddhist Mount Meru cosmology",
    "Homeric Cosmos": "Homeric flat earth cosmology",
    "Hesiodic Cosmos": "Hesiod Theogony cosmology",
    "Pythagorean Cosmos": "Pythagorean harmony spheres",
    "Platonic Cosmos": "Plato Timaeus cosmology",
    "Aristotelian Cosmos": "Aristotelian celestial spheres",
    "Stoic Cosmos": "Stoic cosmology logos",
    "Hermetic Cosmos": "Hermetic Corpus cosmology",
    "Gnostic Pleroma": "Gnostic pleroma cosmology",
    "Neoplatonic Cosmos": "Neoplatonic emanation cosmology",
    "Proclean Cosmos": "Proclus neoplatonic hierarchy",
    "Merkabah Cosmos": "Merkabah mysticism hekhalot",
    "Kabbalistic Tree": "Kabbalistic Tree of Life",
    "Christian Celestial Hierarchy": "Pseudo-Dionysius celestial hierarchy",
    "Great Chain of Being": "Great Chain of Being diagram",
    "Llullian Cosmos": "Ramon Llull combinatorial wheels",
    "Bruno Infinite Cosmos": "Giordano Bruno infinite universe",
    "Theosophical Cosmos": "Theosophy planes of existence",
    "Anthroposophical Cosmos": "Rudolf Steiner anthroposophy",
    "Psychosynthesis": "Roberto Assagioli psychosynthesis star diagram",
    "Piaget Development": "Piaget stages development",
    "Kohlberg Development": "Kohlberg moral development stages",
    "Graves Emergent Cycles": "Clare Graves emergent cyclical levels",
    "Loevinger Ego Development": "Jane Loevinger ego development",
    "Kegan Orders": "Robert Kegan orders of consciousness",
    "Luhmann Social Systems": "Niklas Luhmann social systems",
    "Information Cosmology": "John Wheeler it from bit",
    "Wikidata": "Wikidata logo knowledge graph",
    "OpenAlex": "OpenAlex knowledge graph",
    "Ugaritic Cosmos": "Ugaritic Baal cosmology",
    "Phoenician Cosmos": "Phoenician cosmology Mediterranean",
    "Islamic Falasifa Cosmos": "Ibn Sina Avicenna celestial spheres diagram",
    "Huayan Cosmos": "Huayan four dharmadhatu Fazang diagram",
    "Dzogchen Ground-Path-Fruit": "Dzogchen tantra Tibetan Buddhism thangka",
    "Harranian Sabian Cosmos": "Harran astronomical instruments medieval",
    "Ismaili Emanation Cosmology": "Ismaili cosmology Fatimid diagram",
    "Llullian Cosmos": "Ramon Llull Figure 1 combinatorial wheels",
    "Mazdakite Cosmos": "Sasanian Persia Mazdak social reform",
    "Neo-Confucian Li/Qi Cosmos": "Zhu Xi li qi cosmology diagram",
    "Ojibwe Midewiwin Cosmos": "Midewiwin birch bark scroll diagram",
    "Teotihuacan Cosmic Plan": "Teotihuacan Pyramid of the Sun aerial",
    "Tiantai Three Truths": "Tiantai Buddhism three truths mandala",
    "Turkic Sky Cosmos": "Orkhon inscriptions Tengrism sky",
    "Inuit Layered Cosmos": "Inuit cosmology shaman layers diagram",
    "Dinka Cosmos": "Dinka cattle camp South Sudan ethnography",
    "Amazonian Shamanic Cosmos": "Amazon ayahuasca shaman cosmology painting",
    "Zurvanite Cosmology": "Zurvanite Zoroastrianism",
    "Mazdakite Cosmos": "Mazdak Persian social cosmology",
}


def api_get(base: str, params: dict, *, retries: int = 6) -> dict:
    url = base + "?" + urllib.parse.urlencode({**params, "format": "json"})
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < retries - 1:
                wait = min(60, 5 * (2**attempt))
                print(f"  rate limited — sleeping {wait}s")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("unreachable")


def search_query(row: dict) -> str:
    label = row["cosmograph"]
    if label in SEARCH_OVERRIDES:
        return SEARCH_OVERRIDES[label]
    tradition = row.get("tradition", "")
    if tradition and tradition not in {"Global", "Philosophy", "AI", "Ecology", "Earth Science"}:
        return f"{label} {tradition} cosmology"
    return f"{label} cosmology diagram"


RASTER_HINTS = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", "/thumb/")
NON_RASTER_HINTS = (".pdf", ".djvu", ".tif", ".tiff", ".doc", ".docx")


def is_displayable(url: str) -> bool:
    u = url.lower()
    if any(h in u for h in NON_RASTER_HINTS):
        return False
    return any(h in u for h in RASTER_HINTS)


def normalize_image(hit: dict) -> dict:
    thumb = hit.get("thumbnail_url", "")
    full = hit.get("image_url", "")
    if full and not is_displayable(full) and thumb:
        hit["image_url"] = thumb
    return hit


def needs_fetch(row: dict, *, refetch_bad: bool) -> bool:
    thumb = row.get("thumbnail_url", "")
    if not thumb:
        return True
    if refetch_bad and not is_displayable(row.get("image_url", "")):
        return True
    return False


def license_ok(meta: dict) -> bool:
    license_short = (meta.get("LicenseShortName", {}) or {}).get("value", "")
    usage = (meta.get("UsageTerms", {}) or {}).get("value", "")
    text = f"{license_short} {usage}".lower()
    blocked = ("non-free", "fair use", "copyrighted", "all rights reserved")
    return not any(b in text for b in blocked)


def _score_commons_hit(query: str, title: str, info: dict, meta: dict) -> int:
    if not license_ok(meta) or not info.get("thumburl"):
        return -1
    score = 0
    q_tokens = set(re.findall(r"[a-z0-9]+", query.lower()))
    t_tokens = set(re.findall(r"[a-z0-9]+", title.lower()))
    score += len(q_tokens & t_tokens) * 3
    if any(k in title.lower() for k in ("diagram", "map", "mandala", "cosmos", "cosmology")):
        score += 2
    if "svg" in title.lower():
        score -= 1
    return score


def _commons_search(query: str, *, broad: bool = False) -> dict | None:
    search = query if broad else f"filetype:bitmap {query}"
    data = api_get(
        COMMONS_API,
        {
            "action": "query",
            "generator": "search",
            "gsrsearch": search,
            "gsrnamespace": "6",
            "gsrlimit": "8",
            "prop": "imageinfo",
            "iiprop": "url|thumburl|extmetadata|descriptionurl",
            "iiurlwidth": "640",
        },
    )
    pages = (data.get("query") or {}).get("pages") or {}
    best = None
    best_score = -1
    for page in pages.values():
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata") or {}
        title = page.get("title", "")
        score = _score_commons_hit(query, title, info, meta)
        if score > best_score:
            best_score = score
            best = {
                "thumbnail_url": info["thumburl"],
                "image_url": info.get("url") or info["thumburl"],
                "image_title": title.removeprefix("File:"),
                "image_source": "wikimedia_commons",
                "image_license": (meta.get("LicenseShortName", {}) or {}).get("value", ""),
                "image_page_url": info.get("descriptionurl", ""),
            }
    return best


# Direct Commons file titles when search misses (label → File:…, tried in order).
CURATED_FILES: dict[str, list[str]] = {
    "Amazonian Shamanic Cosmos": [
        "File:Shipibo_concent_art_Icaros.jpg",
        "File:Ayahuasca_Vine.jpg",
        "File:Shaman_in_Ecuador.jpg",
    ],
    "Dinka Cosmos": [
        "File:Cattle of the Dinka people, Juba, South Sudan - 20101230-01.jpg",
        "File:Africa, the Dinka tribe, Bahr-El-Chazal. A group (long legs) Wellcome M0000840.jpg",
    ],
    "Dzogchen Ground-Path-Fruit": [
        "File:Tibetan_Thanka.jpg",
        "File:Tibetan_Buddhist_monks.jpg",
        "File:Dzogchen_Beara.jpg",
    ],
    "Harranian Sabian Cosmos": [
        "File:Harran evleri.jpg",
        "File:Harran-beehouses.jpg",
        "File:Harran beehive houses (1).JPG",
    ],
    "Huayan Cosmos": [
        "File:Kegon.jpg",
        "File:Huayan_Temple.jpg",
        "File:Foguang_Temple.jpg",
    ],
    "Inuit Layered Cosmos": [
        "File:Inukshuk_in_Profile_Park.jpg",
        "File:Inukshuk.jpg",
        "File:Inuit_drummer.jpg",
    ],
    "Islamic Falasifa Cosmos": [
        "File:Avicenna-miniatur.jpg",
        "File:Ibn_Sina_Mausoleum_Hamadan.jpg",
        "File:Avicenna_Title_page_Ibn_Sina.jpg",
    ],
    "Ismaili Emanation Cosmology": ["File:Fatimid_Caliphate.PNG"],
    "Llullian Cosmos": ["File:Ramon_Llull.jpg"],
    "Mazdakite Cosmos": [
        "File:Sassanian Empire cca. 620 A.D.png",
        "File:The Sassanid Persian Empire at it's greatest extent cca. 620 A.D.png",
    ],
    "Neo-Confucian Li/Qi Cosmos": ["File:Zhu_xi.jpg"],
    "Ojibwe Midewiwin Cosmos": [
        "File:General view of a Midewigaan Walter J. Hoffman.png",
        "File:Mide scroll.jpg",
    ],
    "Tiantai Three Truths": ["File:Guoqing_Temple.jpg"],
}


def _commons_by_title(title: str) -> dict | None:
    if not title.startswith("File:"):
        title = f"File:{title}"
    data = api_get(
        COMMONS_API,
        {
            "action": "query",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url|thumburl|extmetadata|descriptionurl",
            "iiurlwidth": "640",
        },
    )
    pages = (data.get("query") or {}).get("pages") or {}
    page = next(iter(pages.values()), {})
    if page.get("missing") is not None:
        return None
    info = (page.get("imageinfo") or [{}])[0]
    if not info.get("thumburl"):
        return None
    meta = info.get("extmetadata") or {}
    if not license_ok(meta):
        return None
    return normalize_image(
        {
            "thumbnail_url": info["thumburl"],
            "image_url": info.get("url") or info["thumburl"],
            "image_title": title.removeprefix("File:"),
            "image_source": "wikimedia_commons_curated",
            "image_license": (meta.get("LicenseShortName", {}) or {}).get("value", ""),
            "image_page_url": info.get("descriptionurl", ""),
        }
    )


def _wikidata_image(label: str) -> dict | None:
    search = api_get(
        WIKIDATA_API,
        {
            "action": "wbsearchentities",
            "search": label,
            "language": "en",
            "limit": "3",
        },
    )
    entities = search.get("search") or []
    for ent in entities:
        qid = ent.get("id")
        if not qid:
            continue
        claims = api_get(
            WIKIDATA_API,
            {"action": "wbgetclaims", "entity": qid, "property": "P18"},
        )
        for claim in (claims.get("claims") or {}).get("P18") or []:
            filename = claim.get("mainsnak", {}).get("datavalue", {}).get("value")
            if not filename:
                continue
            title = filename if filename.startswith("File:") else f"File:{filename}"
            data = api_get(
                COMMONS_API,
                {
                    "action": "query",
                    "titles": title,
                    "prop": "imageinfo",
                    "iiprop": "url|thumburl|extmetadata|descriptionurl",
                    "iiurlwidth": "640",
                },
            )
            pages = (data.get("query") or {}).get("pages") or {}
            page = next(iter(pages.values()), {})
            info = (page.get("imageinfo") or [{}])[0]
            if not info.get("thumburl"):
                continue
            meta = info.get("extmetadata") or {}
            if not license_ok(meta):
                continue
            return {
                "thumbnail_url": info["thumburl"],
                "image_url": info.get("url") or info["thumburl"],
                "image_title": title.removeprefix("File:"),
                "image_source": "wikidata",
                "image_license": (meta.get("LicenseShortName", {}) or {}).get("value", ""),
                "image_page_url": info.get("descriptionurl", ""),
            }
    return None


def pick_image(row: dict) -> dict | None:
    label = row["cosmograph"]
    query = search_query(row)
    queries = [query, label]
    if label in SEARCH_OVERRIDES:
        queries.append(SEARCH_OVERRIDES[label])
    seen: set[str] = set()
    for q in queries:
        if not q or q in seen:
            continue
        seen.add(q)
        hit = _commons_search(q, broad=False)
        if hit:
            return normalize_image(hit)
    hit = _commons_search(label, broad=True)
    if hit:
        return normalize_image(hit)
    wd = _wikidata_image(label)
    if wd:
        return wd
    for title in CURATED_FILES.get(label, []):
        hit = _commons_by_title(title)
        if hit:
            return hit
    return None


def save_catalog(records: list[dict]) -> None:
    CATALOG.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refetch-bad",
        action="store_true",
        help="Re-fetch entries whose image_url is not a displayable raster (e.g. PDF).",
    )
    parser.add_argument(
        "--normalize-only",
        action="store_true",
        help="Fix image_url to thumbnail for existing entries; no API calls.",
    )
    parser.add_argument(
        "--labels",
        nargs="*",
        help="Only process these cosmograph labels.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=2.0,
        help="Seconds between API calls (default: 2).",
    )
    args = parser.parse_args()

    records = json.loads(CATALOG.read_text(encoding="utf-8"))
    if args.normalize_only:
        fixed = 0
        for row in records:
            thumb = row.get("thumbnail_url", "")
            full = row.get("image_url", "")
            if thumb and full and not is_displayable(full):
                row["image_url"] = thumb
                fixed += 1
        save_catalog(records)
        print(f"Normalized {fixed} image_url values", flush=True)
        return

    found = sum(1 for r in records if r.get("thumbnail_url"))
    missed: list[str] = []
    label_filter = set(args.labels or [])
    for i, row in enumerate(records):
        label = row["cosmograph"]
        if label_filter and label not in label_filter:
            continue
        if not needs_fetch(row, refetch_bad=args.refetch_bad):
            if row.get("thumbnail_url") and row.get("image_url"):
                row.update(normalize_image(dict(row)))
            continue
        try:
            img = pick_image(row)
        except Exception as exc:  # noqa: BLE001
            print(f"[{i + 1}/{len(records)}] {label}: ERROR {exc}", flush=True)
            missed.append(label)
            time.sleep(args.sleep)
            continue
        if img:
            row.update(img)
            if not row.get("thumbnail_url"):
                found += 1
            print(f"[{i + 1}/{len(records)}] {label}: {img['image_title'][:60]}", flush=True)
        else:
            missed.append(label)
            print(f"[{i + 1}/{len(records)}] {label}: (no image)", flush=True)
        save_catalog(records)
        time.sleep(args.sleep)
    print(f"\nDone: {found}/{len(records)} with images; {len(missed)} missed", flush=True)
    if missed:
        print("Missed:", ", ".join(missed[:20]), "..." if len(missed) > 20 else "", flush=True)


if __name__ == "__main__":
    main()
