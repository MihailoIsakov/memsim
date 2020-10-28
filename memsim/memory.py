import math


class MemBlock(object):
    """
    A order-n block of the memory hierarchy. In charge of handling a power-of-two amount 
    of pages. 
    """
    def __init__(self, order, address, program=None):
        self.address = address
        self.order   = order
        self.program = program


class BuddyAllocator(object):
    def __init__(self, pages):
        # Check if pages is a power of 2
        if math.log2(pages) % 1 != 0:
            raise NotImplementedError("Support for non-power-of-two zones is not implemented")

        self.pages = pages
        self.MAX_ORDER = math.floor(math.log2(pages))
        # data structure that holds a list of block of every order 
        self.free_areas = [[] for i in range(self.MAX_ORDER + 1)]
        self.free_areas[self.MAX_ORDER].append(MemBlock(order=self.MAX_ORDER, address=0))

    def _split_block(self, order):
        """
        Splits any block of specified order 
        """
        block = self.free_areas[order].pop()

        children = [
            MemBlock(order=block.order - 1, address=block.address, program=block.program),
            MemBlock(order=block.order - 1, address=block.address + 2**(block.order-1), program=block.program),
        ]

        self.free_areas[order - 1] += children

    def _progressive_split(self, order):
        """
        Iteratively splits blocks of order larger than order until there exists a block of order $order.
        """
        if len(self.free_areas[order]) > 0: 
            return 

        # find smallest order that has free blocks
        for search_order in range(order + 1, self.MAX_ORDER + 1):
            if len(self.free_areas[search_order]) == 0 and search_order == self.MAX_ORDER: 
                raise RuntimeError("Cannot create page of order {}".format(order))

            if len(self.free_areas[search_order]) > 0: 
                # go in reverse and split pages
                for reverse_order in range(search_order, order, -1):
                    self._split_block(reverse_order)

                return

    def allocate(self, pages, program):
        """
        Returns a number of RAM page indexes, if enough pages are available.
        Tries to keep pages contiguous. Marks pages as being used by the program.

        Args:
            pages (int): number of pages to allocate
            program (object): simpy agent that is trying to allocate pages

        Returns:
            bool: whether allocation is successful
            list: a list of addresses of blocks allocated, if successful
        """
        order = math.ceil(math.log2(pages))

        if pages != 2**order:
            raise NotImplementedError("Allocating pages which are not powers of two is not supported yet")

        if len(self.free_areas[order]) == 0:
            # if there aren't any blocks of the appropriate size, 
            try: 
                self._progressive_split(order)
            except RuntimeError: 
                return False, []

        block = self.free_areas[order].pop()
        block.program = program
        return True, [block]


    def free(pages, program):
        """
        Frees all provided pages, and groups together contigous regions. 

        Args:
            pages (list): list of used page indexes that should be freed
            program (object): simpy agent that is trying to free pages

        Returns:
            bool: whether allocation is successful
            list: a list of addresses of pages allocated, if successful
        """
        pass