#

class Pattern:
    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        return self.data == other.data

    @classmethod
    def from_list(cls, data):
        return cls(data)

    def as_list(self):
        return self.data
