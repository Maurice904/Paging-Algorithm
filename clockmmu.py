from mmu import MMU


class ClockMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for EscMMU
        self.clock_cache = ClockCache(frames)
        self.is_debug = False
        self.total_disk_reads = 0
        self.total_disk_writes = 0
        self.total_page_faults = 0
        self.dirty_pages = set()

    def set_debug(self):
        self.is_debug = True

    def reset_debug(self):
        self.is_debug = False

    def read_memory(self, page_number):
        flag = self.clock_cache.get(page_number)

        if flag:
            if self.is_debug:
                print(f"READ: page_number -> {page_number} is read from cache, "
                      f"current cache size is {len(self.clock_cache.cache)}")
            return

        # if page_number is not in clock cache
        if self.is_debug:
            print(f"READ: page_number -> {page_number} is NOT in the cache, "
                  f"current cache size is {len(self.clock_cache.cache)}")
        self._replace_page(page_number)

    def write_memory(self, page_number):
        self.dirty_pages.add(page_number)
        if self.is_debug:
            print(f"WRITE: page_number -> {page_number} becomes to a dirty page")
        flag = self.clock_cache.get(page_number)
        #  if page is not in the cache
        if not flag:
            self._replace_page(page_number)

    def _replace_page(self, page_number):
        self.total_disk_reads += 1
        self.total_page_faults += 1

        removed_page = self.clock_cache.push(page_number)
        if removed_page is not None and removed_page in self.dirty_pages:
            self.total_disk_writes += 1
            self.dirty_pages.remove(removed_page)
            if self.is_debug:
                print(f"REPLACE DIRTY PAGE: page_number -> {removed_page} is removed from dirty_pages, "
                      f"current dirty_pages size is {len(self.dirty_pages)}")

    def get_total_disk_reads(self):
        return self.total_disk_reads

    def get_total_disk_writes(self):
        return self.total_disk_writes

    def get_total_page_faults(self):
        return self.total_page_faults


class ClockCache:
    def __init__(self, capacity):
        self.cache = list()  # store key
        self.use_bits = [0] * capacity  # store use bits of keys initialized as 0
        self.capacity = capacity
        self.clock_hand = 0  # pointer

    def push(self, key):
        removed_key = None

        if len(self.cache) < self.capacity:
            self.cache.append(key)
            self.use_bits[self.clock_hand] = 1

        else:
            # finding the first key that needs to be removed from the cache
            while self.use_bits[self.clock_hand] == 1:
                self.use_bits[self.clock_hand] = 0
                self.clock_hand += 1
                self.clock_hand %= self.capacity
            removed_key = self.cache[self.clock_hand]
            self.cache[self.clock_hand] = key
            self.use_bits[self.clock_hand] = 1
        self.clock_hand += 1
        # avoiding the index is out of index range
        self.clock_hand %= self.capacity
        return removed_key

    def get(self, key):
        if key in self.cache:
            idx = self.cache.index(key)
            self.use_bits[idx] = 1
            return True
        return False
