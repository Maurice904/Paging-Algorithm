from mmu import MMU
import random


class RandMMU(MMU):
    def __init__(self, frames):
        self.cache = []
        self.frames = frames
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
        if page_number in self.cache:
            if self.is_debug:
                print(f"READ: page_number -> {page_number} is read from cache, current cache size is {len(self.cache)}")
            return
        if self.is_debug:
            print(f"READ: page_number -> {page_number} is NOT in the cache, current cache size is {len(self.cache)}")
        # page is not in the cache
        self.total_disk_reads += 1
        self.total_page_faults += 1
        # if cache is not full
        if len(self.cache) < self.frames:
            self.cache.append(page_number)
            return
        self._replace_page(page_number)

    def write_memory(self, page_number):
        self.dirty_pages.add(page_number)
        if self.is_debug:
            print(f"WRITE: page_number -> {page_number} becomes to a dirty page")

        if page_number not in self.cache:
            self.total_disk_reads += 1
            self.total_page_faults += 1
            # if cache is not full
            if len(self.cache) < self.frames:
                self.cache.append(page_number)
                return

            self._replace_page(page_number)

    def _replace_page(self, page_number):
        # try to replace a number
        # generate a random number
        random_numer = random.randint(0, len(self.cache) - 1)
        removed_page = self.cache[random_numer]
        if removed_page in self.dirty_pages:
            self.total_disk_writes += 1
            self.dirty_pages.remove(removed_page)
            if self.is_debug:
                print(f"REPLACE DIRTY PAGE: page_number -> {page_number} is removed from dirty_pages, "
                      f"current dirty_pages size is {len(self.dirty_pages)}")
        if self.is_debug:
            print(f"REPLACE: page_number -> {removed_page} is removed from cache")
        self.cache[random_numer] = page_number

    def get_total_disk_reads(self):
        return self.total_disk_reads

    def get_total_disk_writes(self):
        return self.total_disk_writes

    def get_total_page_faults(self):
        return self.total_page_faults
