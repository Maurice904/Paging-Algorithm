from mmu import MMU


class LruMMU(MMU):
    def __init__(self, frames):
        self.lru_cache = LRUCache(capacity=frames)
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
        flag = self.lru_cache.get(page_number)

        if flag:
            if self.is_debug:
                print(f"READ: page_number -> {page_number} is read from cache, "
                      f"current cache size is {len(self.lru_cache.cache)}")
            return

        # if page_number is not in lru cache
        if self.is_debug:
            print(f"READ: page_number -> {page_number} is NOT in the cache, "
                  f"current cache size is {len(self.lru_cache.cache)}")
        self._replace_page(page_number)

    def write_memory(self, page_number):
        self.dirty_pages.add(page_number)
        if self.is_debug:
            print(f"WRITE: page_number -> {page_number} becomes to a dirty page")
        flag = self.lru_cache.get(page_number)

        if not flag:
            self._replace_page(page_number)

    def _replace_page(self, page_number):
        self.total_disk_reads += 1
        self.total_page_faults += 1

        removed_page = self.lru_cache.push(page_number)

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


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = list()

    def push(self, key):
        removed_key = None
        if len(self.cache) < self.capacity:
            self.cache.insert(0, key)
        else:
            removed_key = self.cache.pop()
            self.cache.insert(0, key)

        return removed_key

    def get(self, key):
        if key in self.cache:
            # remove key and then insert it into the head of the list
            self.cache.remove(key)
            self.cache.insert(0, key)
            return True
        return False
