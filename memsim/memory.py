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
    def __init__(self, pages, max_utilization=-1):
        # Check if pages is a power of 2
        if math.log2(pages) % 1 != 0:
            raise NotImplementedError("Support for non-power-of-two zones is not implemented")

        self.num_pages = pages
        self.num_alloc_pages = 0
        self.max_utilization = max_utilization
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

    def _try_combine_block(self, block):
        """
        If a buddy block is free, combines the provided block with the buddy
        """
        buddy = next((b for b in self.free_areas[block.order] if b.address ^ 2**block.order == block.address), None) 

        if buddy is not None:
            self.free_areas[block.order].remove(block)
            self.free_areas[block.order].remove(buddy)
            combined_block = MemBlock(order=block.order + 1, address=min(block.address, buddy.address))
            self.free_areas[block.order + 1].append(combined_block)

            return combined_block
        else:
            return None

    def _progressive_try_combine(self, block):
        """
        Progressively tries to combine a block, and if successful, tries to combine the result.
        """
        while True:
            block = self._try_combine_block(block)
            if block is None:
                break

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
        current_utilization = int((self.num_alloc_pages / self.num_pages) * 100)
        if 0 <= self.max_utilization <= current_utilization:
            # print('Memory utilization ({}%) >= max utilization ({}%)'.format(current_utilization, self.max_utilization))
            return False, [None]
        self.num_alloc_pages += pages
        if len(self.free_areas[order]) == 0:
            # if there aren't any blocks of the appropriate size, 
            try: 
                self._progressive_split(order)
            except RuntimeError: 
                return False, []

        block = self.free_areas[order].pop()
        block.program = program
        return True, [block]


    def free(self, block, program):
        """
        Frees the provided page, and groups together contigous regions. 

        Args:
            page (MemBlock): MemBlock that should be freed
            program (object): simpy agent that is trying to free pages
        """
        block.program = None
        num_pages_freed = 2**block.order
        self.num_alloc_pages -= num_pages_freed
        self.free_areas[block.order].append(block)
        self._progressive_try_combine(block)
