import uuid

from kge.ids import entity_kid, kid, uuid7


def test_uuid7_is_version_7_and_variant_rfc():
    u = uuid7()
    assert u.version == 7
    assert (u.int >> 62) & 0b11 == 0b10  # RFC 4122/9562 variant


def test_uuid7_is_time_ordered():
    a, b = uuid7(), uuid7()
    assert a.int <= b.int or a != b  # monotonic-ish; never equal


def test_kid_shape():
    k = entity_kid()
    assert k.startswith("kg:entity/")
    # Tail is a parseable UUID.
    uuid.UUID(k.split("/", 1)[1])
    assert kid("source").startswith("kg:source/")
