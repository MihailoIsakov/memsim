import simpy

from memsim.memory import BuddyAllocator


def build_environment(pages, max_mem_utilization=-1):
    env = simpy.Environment()
    env.allocator = BuddyAllocator(pages, max_mem_utilization)

    return env
