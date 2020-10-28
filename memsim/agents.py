import abc
import random


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
        self.record_every = 0.5

    def run(self):
        while True:
            print([len(b) for b in self.env.allocator.free_areas])
            yield self.env.timeout(1)


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


        
