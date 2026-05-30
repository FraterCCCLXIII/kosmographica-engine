from kge.models import Base, TrustTier, tier_at_least


def test_metadata_has_core_tables():
    tables = set(Base.metadata.tables)
    assert {"entities", "relationships", "claims", "sources", "claim_sources", "external_ids"} <= tables


def test_tier_ordering():
    assert tier_at_least(TrustTier.EXPERT_ENDORSED, TrustTier.MACHINE_VALIDATED)
    assert tier_at_least(TrustTier.MACHINE_VALIDATED, TrustTier.MACHINE_VALIDATED)
    assert not tier_at_least(TrustTier.MACHINE_UNVERIFIED, TrustTier.MACHINE_VALIDATED)
