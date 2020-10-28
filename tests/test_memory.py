import pytest 

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

    assert len(ba.free_areas[4]) == 0
    assert len(ba.free_areas[3]) == 0
    assert len(ba.free_areas[2]) == 1
    assert len(ba.free_areas[1]) == 0
    assert len(ba.free_areas[0]) == 0

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


