import simpy

from memsim.memory import BuddyAllocator


def build_environment(pages):
    env = simpy.Environment()
    env.allocator = BuddyAllocator(pages)

    return env
