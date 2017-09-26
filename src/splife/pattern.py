#

def char2state(c):
    if c == '.':
        return 0
    elif c == 'O':
        return 1
    else:
        raise ValueError(f"Invalid character '{c}'")

class Pattern:
    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        return all(x == y for x, y in zip(self.data, other.data))

    @classmethod
    def from_list(cls, data):
        return cls(data)

    def as_list(self):
        return self.data

    @classmethod
    def from_txt(cls, txt):
        txt = txt.strip()
        m = None
        data = []
        for line in txt.splitlines():
            if m is None:
                m = len(line)
            else:
                assert len(line) == m
            l = [char2state(c) for c in line]
            data.append(l)
        return cls.from_list(data)

    def as_txt(self):
        return '\n'.join(''.join('.O'[s] for s in l) for l in self.data)
