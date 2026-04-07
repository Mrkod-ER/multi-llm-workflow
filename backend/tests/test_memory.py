from app.engine.memory import MemoryStore


def test_memory_store_write_read():
    mem = MemoryStore()
    mem.write("k1", "value1")
    assert mem.read("k1") == "value1"
    assert mem.read("k2") is None
    assert mem.read("k2", default="fallback") == "fallback"


def test_memory_store_clear():
    mem = MemoryStore()
    mem.write("k1", "value1")
    mem.clear()
    assert mem.read("k1") is None
    assert len(mem.read_all()) == 0
