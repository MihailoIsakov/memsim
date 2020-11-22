import abc
import random
import copy
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import colors as plt_colors


class Program(abc.ABC):
    def __init__(self, env, pid):
        self.env = env
        self.blocks = []
        self._pid = pid
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

    def suicide(self):
        for block in self.blocks:
            self.free(block)

    @abc.abstractmethod
    def run(self):
        pass

    def pid(self):
        return self._pid


class MonitorProgram(Program):
    """
    Agent that does not use the allocator at all, but just logs the current 
    state of memory.
    """
    def __init__(self, env, num_programs, color_array, record_every=1):
        super(MonitorProgram, self).__init__(env, 0)
        self.record_every = record_every
        self.records = []
        self.num_programs = num_programs
        self.alloc_records = []
        raw_colors = np.zeros(shape=(len(color_array), 3))
        for i in range(0, len(color_array)):
            raw_colors[i][0] = color_array[i][0]
            raw_colors[i][1] = color_array[i][1]
            raw_colors[i][2] = color_array[i][2]
        self.color_map = plt_colors.ListedColormap(raw_colors)

    def run(self):
        while True:
            self.records.append(copy.deepcopy(self.env.allocator.free_areas))
            self.alloc_records.append(copy.deepcopy(self.env.allocator.alloc_map))
            yield self.env.timeout(self.record_every)

    def visualize_memory(self): 
        rows = len(self.records)
        cols = self.env.allocator.num_pages

        mem_image = np.zeros(shape=(rows, cols))

        for row, free_areas in enumerate(self.records):
            for order in range(self.env.allocator.MAX_ORDER + 1):
                for block in free_areas[order]:
                    mem_image[row][block.address:block.address + 2**block.order] = 0
        for row, alloc_record in enumerate(self.alloc_records):
            for block_address, block in alloc_record.items():
                mem_image[row][block.address:block.address + 2 ** block.order] = block.pid
        plt.imshow(mem_image, aspect='auto', cmap=self.color_map)
        plt.show()


class StackProgram(Program):
    def __init__(self, env, pid, action_chance=0.5, suicide_chance=0.001):
        super(StackProgram, self).__init__(env, pid)
        self.action_chance = 0.5
        self.suicide_chance = suicide_chance

    def run(self):
        while True:
            if random.random() > (1 - self.action_chance): 
                if random.random() > 0.5: 
                    try: 
                        self.allocate(1)
                    except:
                        pass
                else:
                    if len(self.blocks) > 0:
                        self.free(self.blocks[-1])

            if random.random() < self.suicide_chance:
                self.suicide()

            yield self.env.timeout(1)


class LinkedListProgram(Program):
    def __init__(self, env, pid, action_chance=0.5, block_size=1, suicide_chance=0.001):
        super(LinkedListProgram, self).__init__(env, pid)
        self.action_chance = 0.5
        self.block_size = block_size
        self.suicide_chance = suicide_chance

    def run(self):
        while True:
            if random.random() > (1 - self.action_chance): 
                if random.random() > 0.5: 
                    try: 
                        self.allocate(self.block_size)
                    except:
                        pass
                else:
                    if len(self.blocks) > 0:
                        self.free(random.sample(self.blocks, k=1)[0])

            if random.random() < self.suicide_chance:
                self.suicide()

            yield self.env.timeout(1)

        
class StableLinkedListProgram(Program):
    def __init__(self, pid, env, action_chance=0.5, mean_blocks=100, var_blocks=10, block_size=1, suicide_chance=0.001):
        super(StableLinkedListProgram, self).__init__(env, pid)
        self.action_chance = 0.5
        self.block_size = block_size
        self.suicide_chance = suicide_chance
        self.mean_blocks = mean_blocks
        self.var_blocks = var_blocks

    def run(self):
        while True:
            if random.random() > (1 - self.action_chance): 
                if (random.random() * 2 - 1) > (len(self.blocks) - self.mean_blocks) / self.var_blocks:
                    try: 
                        self.allocate(2**random.randint(0, 5))
                    except:
                        pass
                else:
                    if len(self.blocks) > 0:
                        self.free(random.sample(self.blocks, k=1)[0])

            if random.random() < self.suicide_chance:
                self.suicide()

            yield self.env.timeout(1)


        
        
