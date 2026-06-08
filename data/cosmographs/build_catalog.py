#!/usr/bin/env python3
"""Build catalog.json from CSV + expansion records. Run from repo root."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = Path(__file__).resolve().parent / "catalog.csv"
OUT_PATH = Path(__file__).resolve().parent / "catalog.json"


def parse_year(dates: str) -> int | None:
    if not dates or dates.lower() in {"prehistoric", "global"}:
        return None
    m = re.search(r"(-?\d[\d,]*)\s*BCE", dates, re.I)
    if m:
        return -int(m.group(1).replace(",", ""))
    m = re.search(r"(\d{3,4})", dates)
    if m:
        return int(m.group(1))
    return None


def default_module(tradition: str, typ: str) -> str:
    t = tradition.lower()
    typ_l = typ.lower()
    science_types = {
        "scientific", "psychological", "developmental", "systems", "integral",
        "cognitive", "information", "knowledge", "classification", "evolutionary",
        "complexity", "consciousness", "sociology", "ecological", "philosophical",
    }
    if typ_l in science_types:
        return "philosophy-science"
    indigenous = (
        "paleolithic", "neolithic", "proto-indo", "indigenous", "diné", "lakota",
        "hopi", "iroquois", "anishinaabe", "inuit", "maya", "aztec", "mixtec",
        "toltec", "teotihuacan", "inca", "andean", "muisca", "tupi", "mapuche",
        "amazonian", "yoruba", "kongo", "dogon", "akan", "dinka", "zulu", "nubian",
        "berber", "amazigh", "norse", "ossetian", "sámi", "sami", "turkic",
        "mongolian", "finno-ugric", "shaman", "siberian", "canaanite", "phoenician",
        "mandaean", "manichaean", "babylonian", "sabian", "zoroastrian", "zurvanite",
        "ismaili", "mazdakite", "haudenosaunee", "kushite",
    )
    if any(k in t for k in indigenous):
        return "religion-mythology"
    if typ_l in {"mythic", "mystical", "esoteric", "narrative cosmograph", "topological"}:
        if typ_l in {"mystical", "esoteric", "mythic"}:
            return "religion-mythology"
    return "philosophy-science"


def _article(word: str) -> str:
    return "an" if word[:1].lower() in "aeiou" else "a"


def rich_description(row: dict) -> str:
    """Multi-sentence overview for catalog and entity pages."""
    label = row.get("cosmograph", "This cosmograph").strip()
    tradition = row.get("tradition", "").strip()
    region = row.get("region", "").strip()
    dates = row.get("dates", "").strip()
    typ = row.get("type", "cosmograph").strip().lower()
    domain = row.get("domain", "reality").strip().lower()
    topology = row.get("topology", "structured layers").strip().lower()
    human = row.get("human_position", "participant").strip()
    path = row.get("liberation_path", "").strip()
    sources = row.get("primary_sources", "").strip()

    if tradition and region:
        opener = (
            f"{label} is {_article(typ)} {tradition} {typ} cosmograph from {region}"
        )
    elif tradition:
        opener = f"{label} is {_article(typ)} {tradition} {typ} cosmograph"
    else:
        opener = f"{label} is {_article(typ)} {typ} cosmograph"

    if dates:
        opener += f", attested around {dates}"
    opener += f". It maps the domain of {domain} using {_article(topology)} {topology} topology"
    if human:
        opener += f", placing the human subject as {human.lower()}"
    opener += "."

    sentences = [opener]
    if path and path.lower() not in {"none", "n/a"}:
        sentences.append(
            f"The characteristic path of traversal, salvation, or realization within this map "
            f"is {path.lower()}."
        )
    if sources:
        sentences.append(f"Primary attestation draws on {sources}.")
    return " ".join(sentences)


def default_importance(row: dict) -> str:
    label = row.get("cosmograph", "This cosmograph").strip()
    tradition = row.get("tradition", "").strip()
    typ = row.get("type", "").strip()
    domain = row.get("domain", "").strip()
    topology = row.get("topology", "").strip()
    parts = [f"{label} belongs to the catalog of humanity's maps of reality"]
    if tradition:
        parts.append(f"within the {tradition} tradition")
    if typ and domain:
        parts.append(f"as {_article(typ.lower())} {typ.lower()} chart of {domain.lower()}")
    if topology:
        parts.append(f"structured as {topology.lower()}")
    return ", ".join(parts) + "."


def enrich(label: str, row: dict) -> dict:
    """Add description/importance/module/valid_from where missing."""
    extras = ENRICHMENTS.get(label, {})
    out = dict(row)
    for k, v in extras.items():
        if not out.get(k):
            out[k] = v
    if not out.get("importance"):
        out["importance"] = default_importance(out)
    if not out.get("description"):
        out["description"] = rich_description(out)
    elif len(out["description"]) < 160:
        # Keep curator notes but expand thin one-liners.
        out["description"] = f"{out['description'].rstrip('.')}. {rich_description(out)}"
    if not out.get("module"):
        out["module"] = default_module(out.get("tradition", ""), out.get("type", ""))
    if not out.get("valid_from"):
        out["valid_from"] = parse_year(out.get("dates", ""))
    return out


# description, importance, module overrides
ENRICHMENTS: dict[str, dict] = {
    "Three Worlds": {
        "importance": "Oldest attested tripartite shamanic cosmograph in comparative religion.",
        "module": "religion-mythology",
        "description": (
            "Three Worlds is a Paleolithic shamanic metaphysical cosmograph from Eurasia, attested "
            "from roughly 50,000 BCE onward. It maps the cosmos as vertical layers — upper, middle, "
            "and lower worlds — linked by an axis mundi through which shamans mediate between realms. "
            "The human subject acts as mediator; the path of realization is shamanic ascent. Primary "
            "attestation draws on ethnographic reconstruction of Eurasian shamanism."
        ),
    },
    "World Tree": {
        "importance": "Proto-Indo-European axis mundi motif underlying Eurasian cosmographies.",
        "module": "religion-mythology",
    },
    "Huayan Indra's Net": {
        "importance": "Foundational East Asian network cosmology of mutual interpenetration.",
        "module": "religion-mythology",
        "tradition": "Huayan Buddhism",
        "region": "East Asia",
        "dates": "700 CE+",
        "type": "Metaphysical",
        "domain": "Reality",
        "topology": "Infinite Network",
        "human_position": "Participating node",
        "liberation_path": "Non-dual insight",
        "primary_sources": "Avatamsaka Sutra (Flower Ornament Sutra)",
    },
    "Kalachakra Mandala": {
        "importance": "Among the most complex mandala cosmographs in world religion.",
        "module": "religion-mythology",
        "tradition": "Tibetan Buddhism",
        "region": "Tibet",
        "dates": "1027 CE+",
        "type": "Mystical",
        "domain": "Cosmos",
        "topology": "Mandala",
        "human_position": "Initiate",
        "liberation_path": "Kalachakra initiation",
        "primary_sources": "Kalachakra Tantra",
    },
    "Kongo Cosmogram": {
        "importance": "Central African diasporic cosmograph (Dikenga); four moments of the sun.",
        "module": "religion-mythology",
        "tradition": "Kongo",
        "region": "Central Africa",
        "dates": "1500 CE+",
        "type": "Metaphysical",
        "domain": "Cosmos",
        "topology": "Cross-circle",
        "human_position": "Ancestor-participant",
        "liberation_path": "Ritual remembrance",
        "primary_sources": "Kongo ethnography; Robert Farris Thompson",
    },
    "Popol Vuh Cosmos": {
        "importance": "Maya creation cosmograph linking underworld, earth, and heavens.",
        "module": "religion-mythology",
        "tradition": "Maya",
        "region": "Mesoamerica",
        "dates": "1550 CE",
        "type": "Mythic",
        "domain": "Cosmos",
        "topology": "Vertical Layers",
        "human_position": "Created being",
        "liberation_path": "Heroic journey",
        "primary_sources": "Popol Vuh",
    },
    "Inca Three Worlds": {
        "importance": "Andean hanan-hurin-ukhu pacha tripartite cosmos.",
        "module": "religion-mythology",
        "tradition": "Inca",
        "region": "Andes",
        "dates": "1400 CE",
        "type": "Metaphysical",
        "domain": "Cosmos",
        "topology": "Vertical Layers",
        "human_position": "Community member",
        "liberation_path": "Reciprocity (ayni)",
        "primary_sources": "Inca oral tradition; colonial chronicles",
    },
    "Manichaean Cosmos": {
        "importance": "Major Eurasian dualist cosmograph from Rome to China.",
        "module": "religion-mythology",
        "tradition": "Manichaean",
        "region": "Eurasia",
        "dates": "300 CE",
        "type": "Metaphysical",
        "domain": "Cosmos",
        "topology": "Dualistic Layers",
        "human_position": "Light particle trapped in matter",
        "liberation_path": "Ascent through gnosis",
        "primary_sources": "Manichaean scriptures",
    },
    "Mithraic Cosmos": {
        "importance": "Roman mystery religion with graded cosmic ascent.",
        "module": "religion-mythology",
        "tradition": "Roman Mithraism",
        "region": "Mediterranean",
        "dates": "100 CE",
        "type": "Mystical",
        "domain": "Cosmos",
        "topology": "Planetary Ascent",
        "human_position": "Initiate",
        "liberation_path": "Seven-grade initiation",
        "primary_sources": "Mithraic iconography; Cumont",
    },
    "Yggdrasil": {
        "importance": "Norse world-tree linking nine worlds.",
        "module": "religion-mythology",
        "tradition": "Norse",
        "region": "Scandinavia",
        "dates": "800 CE",
        "type": "Mythic",
        "domain": "Cosmos",
        "topology": "Tree",
        "human_position": "Warrior-soul",
        "liberation_path": "Heroic death and afterlife",
        "primary_sources": "Prose Edda; Poetic Edda",
    },
    "Whitehead Process Cosmos": {
        "importance": "Foundational process-relational cosmology for modern philosophy.",
        "module": "philosophy-science",
        "tradition": "Process Philosophy",
        "region": "Global",
        "dates": "1929",
        "type": "Philosophical",
        "domain": "Reality",
        "topology": "Process Network",
        "human_position": "Actual occasion",
        "liberation_path": "Creative advance",
        "primary_sources": "Whitehead, Process and Reality",
    },
    "Teilhard Noosphere": {
        "importance": "Evolutionary cosmograph culminating in planetary consciousness layer.",
        "module": "philosophy-science",
        "tradition": "Evolutionary Mysticism",
        "region": "Global",
        "dates": "1955",
        "type": "Metaphysical",
        "domain": "Earth",
        "topology": "Layered Evolution",
        "human_position": "Evolutionary agent",
        "liberation_path": "Omega Point convergence",
        "primary_sources": "Teilhard de Chardin, The Phenomenon of Man",
    },
    "Gebser Structures of Consciousness": {
        "importance": "Integral-precursor map of civilizational consciousness structures.",
        "module": "philosophy-science",
        "tradition": "Integral Precursor",
        "region": "Europe",
        "dates": "1949",
        "type": "Developmental",
        "domain": "Consciousness",
        "topology": "Stages",
        "human_position": "Structure-bearer",
        "liberation_path": "Integral transparency",
        "primary_sources": "Jean Gebser, The Ever-Present Origin",
    },
    "Cook-Greuter Ego Development": {
        "importance": "Post-autonomous ego development stages extending Loevinger.",
        "module": "philosophy-science",
        "tradition": "Developmental Psychology",
        "region": "Global",
        "dates": "1999",
        "type": "Developmental",
        "domain": "Ego",
        "topology": "Stages",
        "human_position": "Self",
        "liberation_path": "Ego transcendence",
        "primary_sources": "Cook-Greuter, Postautonomous Ego Development",
    },
    "Yin-Yang Cosmology": {
        "importance": "Foundational Chinese correlative cosmology of dynamic polarity.",
        "module": "religion-mythology",
        "tradition": "Chinese",
        "region": "China",
        "dates": "1000 BCE+",
        "type": "Metaphysical",
        "domain": "Cosmos",
        "topology": "Polarity Cycle",
        "human_position": "Correlative participant",
        "liberation_path": "Harmonization",
        "primary_sources": "Yijing (Book of Changes)",
    },
    "Five Phases Cosmology": {
        "importance": "Wuxing process cosmology mapping transformation across domains.",
        "module": "religion-mythology",
        "tradition": "Chinese",
        "region": "China",
        "dates": "300 BCE",
        "type": "Metaphysical",
        "domain": "Process",
        "topology": "Cycle",
        "human_position": "Embodied correlate",
        "liberation_path": "Balance",
        "primary_sources": "Huainanzi; Huangdi Neijing",
    },
    "Daoist Internal Cosmography": {
        "importance": "Body-as-cosmos map with dantian and internal deities.",
        "module": "religion-mythology",
        "tradition": "Daoist",
        "region": "China",
        "dates": "200 CE+",
        "type": "Psychological",
        "domain": "Body",
        "topology": "Microcosm",
        "human_position": "Cultivator",
        "liberation_path": "Immortality cultivation",
        "primary_sources": "Huangting Jing; Schipper, The Taoist Body",
    },
}

NEW_RECORDS: list[dict] = [
    {"cosmograph": "Ugaritic Cosmos", "tradition": "Canaanite", "region": "Levant", "dates": "1400 BCE", "type": "Metaphysical", "domain": "Cosmos", "topology": "Layered", "human_position": "Servant of Baal", "liberation_path": "Cultic order", "primary_sources": "Ugaritic tablets", "importance": "Direct precursor to Israelite cosmology."},
    {"cosmograph": "Phoenician Cosmos", "tradition": "Phoenician", "region": "Mediterranean", "dates": "1000 BCE", "type": "Metaphysical", "domain": "Cosmos", "topology": "Maritime Disk", "human_position": "Trader-pilgrim", "liberation_path": "Divine patronage", "primary_sources": "Phoenician inscriptions"},
    {"cosmograph": "Mandaean Cosmos", "tradition": "Mandaean", "region": "Mesopotamia", "dates": "200 CE", "type": "Mystical", "domain": "Cosmos", "topology": "Light-Dark Layers", "human_position": "Soul of light", "liberation_path": "Repeated baptism", "primary_sources": "Mandaean Book of John"},
    {"cosmograph": "Chaldean Cosmology", "tradition": "Babylonian", "region": "Mesopotamia", "dates": "500 BCE", "type": "Metaphysical", "domain": "Cosmos", "topology": "Planetary Spheres", "human_position": "Fate-bound soul", "liberation_path": "Astrological knowledge", "primary_sources": "Berossus; later Hermetic astrology"},
    {"cosmograph": "Harranian Sabian Cosmos", "tradition": "Sabian", "region": "Harran", "dates": "900 CE", "type": "Mystical", "domain": "Cosmos", "topology": "Planetary Temples", "human_position": "Philosopher-priest", "liberation_path": "Intellectual ascent", "primary_sources": "Sabian corpus; Thabit ibn Qurra"},
    {"cosmograph": "Bundahishn Universe", "tradition": "Zoroastrian", "region": "Persia", "dates": "900 CE", "type": "Metaphysical", "domain": "Cosmos", "topology": "Layered Creation", "human_position": "Ashavan", "liberation_path": "Frashokereti", "primary_sources": "Bundahishn"},
    {"cosmograph": "Zurvanite Cosmology", "tradition": "Zurvanite", "region": "Persia", "dates": "400 CE", "type": "Metaphysical", "domain": "Time", "topology": "Temporal Dualism", "human_position": "Time-bound soul", "liberation_path": "Choice of allegiance", "primary_sources": "Zurvanite texts"},
    {"cosmograph": "Ismaili Emanation Cosmology", "tradition": "Ismaili", "region": "Islamic World", "dates": "1000 CE", "type": "Mystical", "domain": "Being", "topology": "Emanation Hierarchy", "human_position": "Initiate", "liberation_path": "Progressive initiation", "primary_sources": "Ismaili philosophical corpus"},
    {"cosmograph": "Mazdakite Cosmos", "tradition": "Mazdakite", "region": "Persia", "dates": "500 CE", "type": "Metaphysical", "domain": "Society", "topology": "Egalitarian Layers", "human_position": "Brother", "liberation_path": "Social reform", "primary_sources": "Late antique Persian sources"},
    {"cosmograph": "Dzogchen Ground-Path-Fruit", "tradition": "Tibetan Buddhism", "region": "Tibet", "dates": "800 CE", "type": "Psychological", "domain": "Consciousness", "topology": "Threefold Path", "human_position": "Recognizer", "liberation_path": "Rigpa recognition", "primary_sources": "Dzogchen tantras"},
    {"cosmograph": "Mahamudra Cosmology", "tradition": "Tibetan Buddhism", "region": "Tibet", "dates": "1100 CE", "type": "Psychological", "domain": "Mind", "topology": "Luminosity Layers", "human_position": "Meditator", "liberation_path": "Direct pointing-out", "primary_sources": "Mahamudra lineages"},
    {"cosmograph": "Tibetan Bardo Cosmology", "tradition": "Tibetan Buddhism", "region": "Tibet", "dates": "1300 CE", "type": "Metaphysical", "domain": "Afterlife", "topology": "Bardo Journey", "human_position": "Deceased consciousness", "liberation_path": "Liberation at death", "primary_sources": "Bardo Thodol"},
    {"cosmograph": "Tibetan Medical Cosmology", "tradition": "Tibetan Buddhism", "region": "Tibet", "dates": "1200 CE", "type": "Psychological", "domain": "Body", "topology": "Microcosm-Macrocosm", "human_position": "Patient-healer", "liberation_path": "Balance of humors", "primary_sources": "Gyushi (Four Tantras)"},
    {"cosmograph": "Tiantai Three Truths", "tradition": "Tiantai", "region": "China", "dates": "600 CE", "type": "Metaphysical", "domain": "Reality", "topology": "Threefold Truth", "human_position": "Contemplative", "liberation_path": "Perfect enlightenment", "primary_sources": "Zhiyi, Mohe Zhiguan"},
    {"cosmograph": "Tendai Cosmos", "tradition": "Tendai", "region": "Japan", "dates": "800 CE", "type": "Metaphysical", "domain": "Cosmos", "topology": "One Vehicle", "human_position": "Practitioner", "liberation_path": "Enlightenment in this body", "primary_sources": "Saicho; Tendai synthesis"},
    {"cosmograph": "Shingon Mandala Universe", "tradition": "Shingon", "region": "Japan", "dates": "900 CE", "type": "Mystical", "domain": "Cosmos", "topology": "Mandala", "human_position": "Initiate", "liberation_path": "Esoteric ritual", "primary_sources": "Kukai; Shingon tantras"},
    {"cosmograph": "Neo-Confucian Li/Qi Cosmos", "tradition": "Neo-Confucian", "region": "East Asia", "dates": "1100 CE", "type": "Philosophical", "domain": "Reality", "topology": "Principle-Matter", "human_position": "Sage-in-training", "liberation_path": "Self-cultivation", "primary_sources": "Zhu Xi; Wang Yangming"},
    {"cosmograph": "Korean Seon Cosmology", "tradition": "Korean Seon", "region": "Korea", "dates": "1200 CE", "type": "Psychological", "domain": "Mind", "topology": "Sudden Awakening", "human_position": "Meditator", "liberation_path": "Hwadu inquiry", "primary_sources": "Korean Seon tradition"},
    {"cosmograph": "Navajo Emergence Cosmology", "tradition": "Diné", "region": "North America", "dates": "Prehistoric", "type": "Mythic", "domain": "Cosmos", "topology": "Emergence Journey", "human_position": "Emergent being", "liberation_path": "Ceremonial restoration", "primary_sources": "Diné emergence narratives"},
    {"cosmograph": "Lakota Sacred Hoop", "tradition": "Lakota", "region": "North America", "dates": "Prehistoric", "type": "Metaphysical", "domain": "Community", "topology": "Sacred Circle", "human_position": "Relative", "liberation_path": "Harmony (wo Lakota)", "primary_sources": "Lakota oral tradition"},
    {"cosmograph": "Hopi World Ages", "tradition": "Hopi", "region": "North America", "dates": "Prehistoric", "type": "Mythic", "domain": "Cosmos", "topology": "Cyclic Worlds", "human_position": "Clan member", "liberation_path": "Ceremonial continuity", "primary_sources": "Hopi tradition"},
    {"cosmograph": "Haudenosaunee Sky World", "tradition": "Haudenosaunee", "region": "North America", "dates": "Prehistoric", "type": "Mythic", "domain": "Cosmos", "topology": "Sky-Earth Layers", "human_position": "Clan kin", "liberation_path": "Reciprocity", "primary_sources": "Haudenosaunee creation stories"},
    {"cosmograph": "Ojibwe Midewiwin Cosmos", "tradition": "Anishinaabe", "region": "North America", "dates": "1700 CE", "type": "Mystical", "domain": "Cosmos", "topology": "Medicine Lodge", "human_position": "Initiate", "liberation_path": "Midewiwin degrees", "primary_sources": "Midewiwin birchbark scrolls"},
    {"cosmograph": "Inuit Layered Cosmos", "tradition": "Inuit", "region": "Arctic", "dates": "Prehistoric", "type": "Mythic", "domain": "Cosmos", "topology": "Vertical Layers", "human_position": "Hunter-shaman", "liberation_path": "Shamanic travel", "primary_sources": "Inuit oral tradition"},
    {"cosmograph": "Aztec 13 Heavens", "tradition": "Aztec", "region": "Mesoamerica", "dates": "1400 CE", "type": "Metaphysical", "domain": "Heaven", "topology": "Thirteen Layers", "human_position": "Warrior-soul", "liberation_path": "Solar afterlife", "primary_sources": "Aztec codices"},
    {"cosmograph": "Aztec 9 Underworlds", "tradition": "Aztec", "region": "Mesoamerica", "dates": "1400 CE", "type": "Metaphysical", "domain": "Underworld", "topology": "Nine Layers", "human_position": "Soul traveler", "liberation_path": "Four-year journey", "primary_sources": "Aztec codices"},
    {"cosmograph": "Mixtec Cosmology", "tradition": "Mixtec", "region": "Mesoamerica", "dates": "1200 CE", "type": "Mythic", "domain": "Cosmos", "topology": "Genealogical-Time", "human_position": "Dynastic actor", "liberation_path": "Ancestral alignment", "primary_sources": "Mixtec codices"},
    {"cosmograph": "Toltec Cosmology", "tradition": "Toltec", "region": "Mesoamerica", "dates": "900 CE", "type": "Mythic", "domain": "Cosmos", "topology": "Sacred city", "human_position": "Warrior-priest", "liberation_path": "Teotihuacan ascent myth", "primary_sources": "Toltec-Aztec synthesis"},
    {"cosmograph": "Teotihuacan Cosmic Plan", "tradition": "Teotihuacan", "region": "Mesoamerica", "dates": "200 CE", "type": "Topological", "domain": "Cosmos", "topology": "Urban Axis", "human_position": "Citizen", "liberation_path": "Processional alignment", "primary_sources": "Teotihuacan archaeology"},
    {"cosmograph": "Andean Chakana", "tradition": "Andean", "region": "South America", "dates": "Prehistoric", "type": "Metaphysical", "domain": "Cosmos", "topology": "Cross-Quarters", "human_position": "Ayllu member", "liberation_path": "Reciprocity", "primary_sources": "Andean ethnography"},
    {"cosmograph": "Muisca Cosmos", "tradition": "Muisca", "region": "Colombia", "dates": "1200 CE", "type": "Metaphysical", "domain": "Cosmos", "topology": "Lake-Center", "human_position": "Zipa-subject", "liberation_path": "Gold offering", "primary_sources": "Muisca chronicles"},
    {"cosmograph": "Tupi-Guarani Cosmos", "tradition": "Tupi-Guarani", "region": "Brazil", "dates": "Prehistoric", "type": "Mythic", "domain": "Cosmos", "topology": "Land without Evil", "human_position": "Wanderer", "liberation_path": "Migration to paradise", "primary_sources": "Tupi-Guarani tradition"},
    {"cosmograph": "Mapuche Cosmos", "tradition": "Mapuche", "region": "Chile", "dates": "Prehistoric", "type": "Mythic", "domain": "Cosmos", "topology": "Nuke Mapu", "human_position": "Machi-guided", "liberation_path": "Ritual balance", "primary_sources": "Mapuche oral tradition"},
    {"cosmograph": "Amazonian Shamanic Cosmos", "tradition": "Amazonian", "region": "South America", "dates": "Prehistoric", "type": "Metaphysical", "domain": "Cosmos", "topology": "Vertical Layers", "human_position": "Shaman", "liberation_path": "Plant-spirit alliance", "primary_sources": "Amazonian ethnography"},
    {"cosmograph": "Yoruba Cosmos", "tradition": "Yoruba", "region": "West Africa", "dates": "Prehistoric", "type": "Metaphysical", "domain": "Cosmos", "topology": "Orisha Domains", "human_position": "Devotee", "liberation_path": "Iwa pele", "primary_sources": "Ifa corpus"},
    {"cosmograph": "Dogon Universe", "tradition": "Dogon", "region": "West Africa", "dates": "Prehistoric", "type": "Metaphysical", "domain": "Cosmos", "topology": "Nommo Cosmology", "human_position": "Initiate", "liberation_path": "Ritual knowledge", "primary_sources": "Griaule; Dogon tradition"},
    {"cosmograph": "Akan Cosmos", "tradition": "Akan", "region": "West Africa", "dates": "Prehistoric", "type": "Metaphysical", "domain": "Cosmos", "topology": "Ancestor Realm", "human_position": "Lineage member", "liberation_path": "Ancestral honor", "primary_sources": "Akan tradition"},
    {"cosmograph": "Dinka Cosmos", "tradition": "Dinka", "region": "East Africa", "dates": "Prehistoric", "type": "Mythic", "domain": "Cosmos", "topology": "Cattle-Heaven Link", "human_position": "Herder", "liberation_path": "Divine covenant", "primary_sources": "Dinka oral tradition"},
    {"cosmograph": "Zulu Cosmos", "tradition": "Zulu", "region": "Southern Africa", "dates": "Prehistoric", "type": "Mythic", "domain": "Cosmos", "topology": "Ancestor Sky", "human_position": "Clan member", "liberation_path": "Ukubonga", "primary_sources": "Zulu oral tradition"},
    {"cosmograph": "Ancient Nubian Cosmos", "tradition": "Kushite", "region": "Nubia", "dates": "2000 BCE", "type": "Metaphysical", "domain": "Cosmos", "topology": "Nile Layers", "human_position": "Pharaoh-subject", "liberation_path": "Afterlife cult", "primary_sources": "Nubian archaeology"},
    {"cosmograph": "Berber Cosmology", "tradition": "Amazigh", "region": "North Africa", "dates": "Prehistoric", "type": "Mythic", "domain": "Cosmos", "topology": "Mountain-Sky", "human_position": "Tribe member", "liberation_path": "Ancestral law", "primary_sources": "Amazigh oral tradition"},
    {"cosmograph": "Nart Cosmos", "tradition": "Ossetian", "region": "Caucasus", "dates": "Prehistoric", "type": "Mythic", "domain": "Cosmos", "topology": "Heroic Cycle", "human_position": "Nart hero", "liberation_path": "Heroic death", "primary_sources": "Nart sagas"},
    {"cosmograph": "Sámi Cosmos", "tradition": "Sámi", "region": "Fennoscandia", "dates": "Prehistoric", "type": "Mythic", "domain": "Cosmos", "topology": "Noaidi Worlds", "human_position": "Noaidi", "liberation_path": "Drum journey", "primary_sources": "Sámi tradition"},
    {"cosmograph": "Turkic Sky Cosmos", "tradition": "Turkic", "region": "Central Asia", "dates": "500 CE", "type": "Metaphysical", "domain": "Cosmos", "topology": "Sky-Earth Axis", "human_position": "Khan-subject", "liberation_path": "Tengri alignment", "primary_sources": "Orkhon inscriptions"},
    {"cosmograph": "Mongolian Shamanic Cosmos", "tradition": "Mongolian", "region": "Central Asia", "dates": "1200 CE", "type": "Metaphysical", "domain": "Cosmos", "topology": "Three Worlds", "human_position": "Shaman", "liberation_path": "Spirit flight", "primary_sources": "Mongolian shamanism"},
    {"cosmograph": "Finno-Ugric World Tree", "tradition": "Finno-Ugric", "region": "Northern Eurasia", "dates": "Prehistoric", "type": "Mythic", "domain": "Cosmos", "topology": "Tree", "human_position": "Shaman", "liberation_path": "Axis ascent", "primary_sources": "Finno-Ugric folklore"},
    {"cosmograph": "Sefer Yetzirah Cosmos", "tradition": "Jewish", "region": "Levant", "dates": "200 CE", "type": "Mystical", "domain": "Creation", "topology": "Letter-Structure", "human_position": "Contemplative", "liberation_path": "Combinatorial meditation", "primary_sources": "Sefer Yetzirah"},
    {"cosmograph": "Jacob Boehme Cosmos", "tradition": "Christian Theosophy", "region": "Europe", "dates": "1600 CE", "type": "Esoteric", "domain": "Being", "topology": "Divine Wrath-Love", "human_position": "Soul in tension", "liberation_path": "Rebirth in Christ", "primary_sources": "Jacob Boehme, Aurora"},
    {"cosmograph": "Swedenborg Cosmos", "tradition": "Swedenborgian", "region": "Europe", "dates": "1750 CE", "type": "Mystical", "domain": "Heaven", "topology": "Correspondences", "human_position": "Spirit", "liberation_path": "Regeneration", "primary_sources": "Emanuel Swedenborg, Heaven and Hell"},
    {"cosmograph": "Rosicrucian Universe", "tradition": "Rosicrucian", "region": "Europe", "dates": "1600 CE", "type": "Esoteric", "domain": "Cosmos", "topology": "Alchemical Hierarchy", "human_position": "Initiate", "liberation_path": "Spiritual alchemy", "primary_sources": "Rosicrucian manifestos"},
    {"cosmograph": "Golden Dawn Tree", "tradition": "Hermetic Order of Golden Dawn", "region": "Europe", "dates": "1888", "type": "Esoteric", "domain": "Being", "topology": "Tree of Life", "human_position": "Adept", "liberation_path": "Grade ascent", "primary_sources": "Golden Dawn teachings"},
    {"cosmograph": "Thelemic Cosmology", "tradition": "Thelema", "region": "Global", "dates": "1904", "type": "Esoteric", "domain": "Will", "topology": "Aeonic", "human_position": "Thelemite", "liberation_path": "True Will", "primary_sources": "Aleister Crowley, Book of the Law"},
    {"cosmograph": "Bergson Evolutionary Cosmos", "tradition": "Philosophy", "region": "Europe", "dates": "1907", "type": "Philosophical", "domain": "Time", "topology": "Creative Duration", "human_position": "Living duration", "liberation_path": "Intuition", "primary_sources": "Henri Bergson, Creative Evolution"},
    {"cosmograph": "Deep Ecology", "tradition": "Ecology", "region": "Global", "dates": "1973", "type": "Ecological", "domain": "Earth", "topology": "Ecocentric Web", "human_position": "Ecological self", "liberation_path": "Self-realization", "primary_sources": "Arne Naess"},
    {"cosmograph": "Earth System Science", "tradition": "Earth Science", "region": "Global", "dates": "1980", "type": "Scientific", "domain": "Earth", "topology": "Coupled Systems", "human_position": "Observer-agent", "liberation_path": "Sustainability", "primary_sources": "NASA Earth system science"},
    {"cosmograph": "Planetary Boundaries", "tradition": "Resilience Science", "region": "Global", "dates": "2009", "type": "Ecological", "domain": "Earth", "topology": "Threshold Map", "human_position": "Steward", "liberation_path": "Safe operating space", "primary_sources": "Stockholm Resilience Centre"},
    {"cosmograph": "Cellular Automata Universe", "tradition": "Computational", "region": "Global", "dates": "2002", "type": "Cognitive", "domain": "Computation", "topology": "Automaton Grid", "human_position": "Pattern", "liberation_path": "Emergent complexity", "primary_sources": "Stephen Wolfram, A New Kind of Science"},
    {"cosmograph": "Computational Universe", "tradition": "Digital Physics", "region": "Global", "dates": "1980", "type": "Information", "domain": "Reality", "topology": "Cellular Automaton", "human_position": "Computed state", "liberation_path": "Knowledge", "primary_sources": "Edward Fredkin"},
    {"cosmograph": "Digital Physics", "tradition": "Digital Physics", "region": "Global", "dates": "1969", "type": "Information", "domain": "Reality", "topology": "Discrete Computation", "human_position": "Program state", "liberation_path": "Knowledge", "primary_sources": "Konrad Zuse, Calculating Space"},
    {"cosmograph": "Constructor Theory", "tradition": "Physics", "region": "Global", "dates": "2012", "type": "Scientific", "domain": "Reality", "topology": "Possible-Impossible", "human_position": "Constructor", "liberation_path": "Knowledge", "primary_sources": "David Deutsch, Constructor Theory"},
    {"cosmograph": "Free Energy Principle", "tradition": "Neuroscience", "region": "Global", "dates": "2006", "type": "Psychological", "domain": "Mind", "topology": "Markov Blanket", "human_position": "Self-model", "liberation_path": "Minimize surprise", "primary_sources": "Karl Friston"},
    {"cosmograph": "Actor-Network Theory", "tradition": "Science Studies", "region": "Global", "dates": "1984", "type": "Systems", "domain": "Society", "topology": "Heterogeneous Network", "human_position": "Actant", "liberation_path": "Translation", "primary_sources": "Bruno Latour"},
    {"cosmograph": "Connectomics", "tradition": "Neuroscience", "region": "Global", "dates": "2005", "type": "Scientific", "domain": "Brain", "topology": "Connectome Graph", "human_position": "Neural network", "liberation_path": "Mapping", "primary_sources": "Seung; Human Connectome Project"},
    {"cosmograph": "Symbolic Knowledge Graphs", "tradition": "AI", "region": "Global", "dates": "1980", "type": "Cognitive", "domain": "Knowledge", "topology": "Semantic Network", "human_position": "Reasoner", "liberation_path": "Inference", "primary_sources": "Early AI; Cyc"},
    {"cosmograph": "Connectionist Networks", "tradition": "AI", "region": "Global", "dates": "1986", "type": "Cognitive", "domain": "Mind", "topology": "Neural Network", "human_position": "Pattern learner", "liberation_path": "Training", "primary_sources": "Rumelhart & McClelland, PDP volumes"},
    {"cosmograph": "AI-generated Knowledge Graphs", "tradition": "AI", "region": "Global", "dates": "2023", "type": "Cognitive", "domain": "Knowledge", "topology": "Dynamic Graph", "human_position": "Curator", "liberation_path": "Verification", "primary_sources": "LLM extraction pipelines"},
    {"cosmograph": "Maya World Tree", "tradition": "Maya", "region": "Mesoamerica", "dates": "Prehistoric", "type": "Mythic", "domain": "Cosmos", "topology": "World Tree", "human_position": "Living being", "liberation_path": "Cosmic renewal", "primary_sources": "Maya iconography"},
    {"cosmograph": "Huayan Cosmos", "tradition": "Huayan Buddhism", "region": "East Asia", "dates": "700 CE+", "type": "Metaphysical", "domain": "Reality", "topology": "Four Dharmadhatus", "human_position": "Bodhisattva", "liberation_path": "Interpenetration insight", "primary_sources": "Avatamsaka Sutra; Fazang"},
    {"cosmograph": "Huayan Indra's Net", "tradition": "Huayan Buddhism", "region": "East Asia", "dates": "700 CE+", "type": "Metaphysical", "domain": "Reality", "topology": "Infinite Network", "human_position": "Participating node", "liberation_path": "Non-dual insight", "primary_sources": "Avatamsaka Sutra (Flower Ornament Sutra)"},
    {"cosmograph": "Kalachakra Mandala", "tradition": "Tibetan Buddhism", "region": "Tibet", "dates": "1027 CE+", "type": "Mystical", "domain": "Cosmos", "topology": "Mandala", "human_position": "Initiate", "liberation_path": "Kalachakra initiation", "primary_sources": "Kalachakra Tantra"},
    {"cosmograph": "Kongo Cosmogram", "tradition": "Kongo", "region": "Central Africa", "dates": "1500 CE+", "type": "Metaphysical", "domain": "Cosmos", "topology": "Cross-circle", "human_position": "Ancestor-participant", "liberation_path": "Ritual remembrance", "primary_sources": "Kongo ethnography; Robert Farris Thompson"},
    {"cosmograph": "Popol Vuh Cosmos", "tradition": "Maya", "region": "Mesoamerica", "dates": "1550 CE", "type": "Mythic", "domain": "Cosmos", "topology": "Vertical Layers", "human_position": "Created being", "liberation_path": "Heroic journey", "primary_sources": "Popol Vuh"},
    {"cosmograph": "Inca Three Worlds", "tradition": "Inca", "region": "Andes", "dates": "1400 CE", "type": "Metaphysical", "domain": "Cosmos", "topology": "Vertical Layers", "human_position": "Community member", "liberation_path": "Reciprocity (ayni)", "primary_sources": "Inca oral tradition; colonial chronicles"},
    {"cosmograph": "Manichaean Cosmos", "tradition": "Manichaean", "region": "Eurasia", "dates": "300 CE", "type": "Metaphysical", "domain": "Cosmos", "topology": "Dualistic Layers", "human_position": "Light particle trapped in matter", "liberation_path": "Ascent through gnosis", "primary_sources": "Manichaean scriptures"},
    {"cosmograph": "Mithraic Cosmos", "tradition": "Roman Mithraism", "region": "Mediterranean", "dates": "100 CE", "type": "Mystical", "domain": "Cosmos", "topology": "Planetary Ascent", "human_position": "Initiate", "liberation_path": "Seven-grade initiation", "primary_sources": "Mithraic iconography; Cumont"},
    {"cosmograph": "Yggdrasil", "tradition": "Norse", "region": "Scandinavia", "dates": "800 CE", "type": "Mythic", "domain": "Cosmos", "topology": "Tree", "human_position": "Warrior-soul", "liberation_path": "Heroic death and afterlife", "primary_sources": "Prose Edda; Poetic Edda"},
    {"cosmograph": "Whitehead Process Cosmos", "tradition": "Process Philosophy", "region": "Global", "dates": "1929", "type": "Philosophical", "domain": "Reality", "topology": "Process Network", "human_position": "Actual occasion", "liberation_path": "Creative advance", "primary_sources": "Whitehead, Process and Reality"},
    {"cosmograph": "Teilhard Noosphere", "tradition": "Evolutionary Mysticism", "region": "Global", "dates": "1955", "type": "Metaphysical", "domain": "Earth", "topology": "Layered Evolution", "human_position": "Evolutionary agent", "liberation_path": "Omega Point convergence", "primary_sources": "Teilhard de Chardin, The Phenomenon of Man"},
    {"cosmograph": "Gebser Structures of Consciousness", "tradition": "Integral Precursor", "region": "Europe", "dates": "1949", "type": "Developmental", "domain": "Consciousness", "topology": "Stages", "human_position": "Structure-bearer", "liberation_path": "Integral transparency", "primary_sources": "Jean Gebser, The Ever-Present Origin"},
    {"cosmograph": "Cook-Greuter Ego Development", "tradition": "Developmental Psychology", "region": "Global", "dates": "1999", "type": "Developmental", "domain": "Ego", "topology": "Stages", "human_position": "Self", "liberation_path": "Ego transcendence", "primary_sources": "Cook-Greuter, Postautonomous Ego Development"},
    {"cosmograph": "Yin-Yang Cosmology", "tradition": "Chinese", "region": "China", "dates": "1000 BCE+", "type": "Metaphysical", "domain": "Cosmos", "topology": "Polarity Cycle", "human_position": "Correlative participant", "liberation_path": "Harmonization", "primary_sources": "Yijing (Book of Changes)"},
    {"cosmograph": "Five Phases Cosmology", "tradition": "Chinese", "region": "China", "dates": "300 BCE", "type": "Metaphysical", "domain": "Process", "topology": "Cycle", "human_position": "Embodied correlate", "liberation_path": "Balance", "primary_sources": "Huainanzi; Huangdi Neijing"},
    {"cosmograph": "Daoist Internal Cosmography", "tradition": "Daoist", "region": "China", "dates": "200 CE+", "type": "Psychological", "domain": "Body", "topology": "Microcosm", "human_position": "Cultivator", "liberation_path": "Immortality cultivation", "primary_sources": "Huangting Jing; Schipper, The Taoist Body"},
    {"cosmograph": "Transformer Latent Spaces", "tradition": "AI", "region": "Global", "dates": "2017+", "type": "Cognitive", "domain": "Meaning", "topology": "High-Dimensional Latent", "human_position": "Prompt engineer", "liberation_path": "Alignment", "primary_sources": "Attention Is All You Need; GPT papers"},
    {"cosmograph": "World Models", "tradition": "AI", "region": "Global", "dates": "2023+", "type": "Cognitive", "domain": "Reality", "topology": "Predictive Model", "human_position": "Agent", "liberation_path": "Planning", "primary_sources": "Contemporary world-model research"},
    {"cosmograph": "Agentic Societies", "tradition": "AI", "region": "Global", "dates": "2023+", "type": "Cognitive", "domain": "Society", "topology": "Multi-Agent Graph", "human_position": "Orchestrator", "liberation_path": "Coordination", "primary_sources": "Multi-agent LLM systems"},
    {"cosmograph": "Knowledge Graphs", "tradition": "Semantic Web", "region": "Global", "dates": "2000+", "type": "Knowledge", "domain": "Knowledge", "topology": "RDF Graph", "human_position": "Curator", "liberation_path": "Linked data", "primary_sources": "Semantic Web stack"},
    {"cosmograph": "Indra's Net", "tradition": "Huayan Buddhism", "region": "East Asia", "dates": "700 CE+", "type": "Metaphysical", "domain": "Reality", "topology": "Infinite Network", "human_position": "Jewel-node", "liberation_path": "Mutual causality", "primary_sources": "Avatamsaka Sutra"},
]


def load_csv() -> list[dict]:
    rows = []
    with CSV_PATH.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def main() -> None:
    by_label: dict[str, dict] = {}
    for row in load_csv():
        by_label[row["cosmograph"]] = row
    for row in NEW_RECORDS:
        by_label[row["cosmograph"]] = row

    records = [enrich(label, row) for label, row in sorted(by_label.items(), key=lambda x: x[0])]
    OUT_PATH.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(records)} records to {OUT_PATH}")


if __name__ == "__main__":
    main()
