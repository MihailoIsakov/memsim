import abc
import random
import copy
import numpy as np

import matplotlib.pyplot as plt


class Program(abc.ABC):
    def __init__(self, env):
        self.env = env
        self.blocks = []
        # Start the run process everytime an instance is created.
        self.action = env.process(self.run())


    def allocate(self, pages):
        """
        The program asks the environment to allocate a number of pages
        """
        success, blocks = self.env.allocator.allocate(pages, program=self)
        if success:
            self.blocks += blocks
        else:
            raise NotImplementedError("Should implement handling failed allocations")

    def free(self, block):
        self.blocks.remove(block)
        self.env.allocator.free(block, program=self)

    @abc.abstractmethod
    def run(self):
        pass


class MonitorProgram(Program):
    """
    Agent that does not use the allocator at all, but just logs the current 
    state of memory.
    """
    def __init__(self, env, record_every=1):
        super(MonitorProgram, self).__init__(env)
        self.record_every = record_every
        self.records = []

    def run(self):
        while True:
            self.records.append(copy.deepcopy(self.env.allocator.free_areas))
            yield self.env.timeout(self.record_every)

    def visualize_memory(self): 
        rows = len(self.records)
        cols = self.env.allocator.pages

        mem_image = np.zeros((rows, cols))

        for row, free_areas in enumerate(self.records):
            for order in range(self.env.allocator.MAX_ORDER + 1):
                for block in free_areas[order]:
                    mem_image[row][block.address:block.address + 2**block.order] = 1

        plt.imshow(mem_image)
        plt.show()


class StackProgram(Program):
    def __init__(self, env, action_chance=0.5):
        super(StackProgram, self).__init__(env)
        self.action_chance = 0.5

    def run(self):
        while True:
            if random.random() > self.action_chance: 
                if random.random() > 0.5: 
                    try: 
                        self.allocate(1)
                    except:
                        pass
                else:
                    if len(self.blocks) > 0:
                        self.free(self.blocks[-1])

            yield self.env.timeout(1)


        
