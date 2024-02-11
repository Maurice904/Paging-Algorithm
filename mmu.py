'''
* Interface for Memory Management Unit.
* The memory management unit should maintain the concept of a page table.
* As pages are read and written to, this changes the pages loaded into the
* the limited number of frames. The MMU keeps records, which will be used
* to analyse the performance of different replacement strategies implemented
* for the MMU.
*
'''
from abc import ABCMeta, abstractmethod


class MMU(metaclass=ABCMeta):
    @abstractmethod
    def read_memory(self, page_number):
        pass

    @abstractmethod
    def write_memory(self, page_number):
        pass

    @abstractmethod
    def set_debug(self):
        pass

    @abstractmethod
    def reset_debug(self):
        pass

    @abstractmethod
    def get_total_disk_reads(self):
        return -1

    @abstractmethod
    def get_total_disk_writes(self):
        return -1

    @abstractmethod
    def get_total_page_faults(self):
        return -1
