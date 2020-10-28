from memsim.memory import BuddyAllocator


def test_splitting():
    ba = BuddyAllocator(16)

    ba._progressive_split(1)
    assert len(ba.free_areas[1]) == 2

    ba._progressive_split(0)
    assert len(ba.free_areas[0]) == 2
    assert len(ba.free_areas[1]) == 1


def test_allocate():
    ba = BuddyAllocator(16)

    succ4, pages4 = ba.allocate(4, "program4")
    succ8, pages8 = ba.allocate(8, "program8")

    assert all([a == b for a, b in zip([len(x) for x in ba.free_areas], [0, 0, 1, 0, 0])])

    assert pages4[0].order == 2
    assert pages8[0].order == 3


def test_fail_to_allocate():
    ba = BuddyAllocator(16)

    succ4, _ = ba.allocate(4, "program4")
    assert succ4 
    succ8, _ = ba.allocate(8, "program8")
    assert succ8
    succ8, _ = ba.allocate(8, "program8")
    assert succ8 is False


def test_free1():
    ba = BuddyAllocator(16)

    succ4, block4 = ba.allocate(4, "program4")
    assert succ4 
    succ8, block8 = ba.allocate(8, "program8")
    assert succ8
    succ1, block1 = ba.allocate(1, "program1")
    assert succ1

    ba.free(block4[0], "program4")
    assert all([a == b for a, b in zip([len(x) for x in ba.free_areas], [1, 1, 1, 0, 0])])


def test_free2():
    ba = BuddyAllocator(16)

    for i in range(10):
        succ1, block1 = ba.allocate(1, "program1")
        ba.free(block1[0], "program1")

    assert all([a == b for a, b in zip([len(x) for x in ba.free_areas], [0, 0, 0, 0, 1])])
