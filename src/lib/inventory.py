from collections import defaultdict


class Inventory(defaultdict):
    def __init__(self):
        super().__init__(lambda: 0)
