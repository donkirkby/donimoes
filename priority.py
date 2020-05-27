from heapq import heappush, heappop


class PriorityQueue:
    def __init__(self):
        self.item_heap = []  # [ [priority, item] ]
        self.dummy = '<dummy entry>'
        self.item_dict = {}  # { item: [priority, item] }

    def __bool__(self):
        return bool(self.item_dict)

    def add(self, item, priority=0):
        try:
            self.remove(item)
        except KeyError:
            pass
        wrapper = [priority, item]
        heappush(self.item_heap, wrapper)
        self.item_dict[item] = wrapper

    def remove(self, item):
        wrapper = self.item_dict[item]
        wrapper[1] = self.dummy

    def pop(self):
        while True:
            if not self.item_heap:
                raise KeyError('pop from an empty priority queue')
            wrapper = heappop(self.item_heap)
            item = wrapper[1]
            if item is not self.dummy:
                break
        del self.item_dict[item]
        return wrapper[1]
