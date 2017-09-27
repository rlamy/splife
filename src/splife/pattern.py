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

    @property
    def height(self):
        return len(self.data)


    @property
    def width(self):
        return len(self.data[0])

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

def successor(patt):
    h = patt.height
    l = patt.width
    new_p = Pattern([[0] * l for _ in range(h)])
    for i in range(h):
        rows = patt.data[max(i - 1, 0):i + 2]
        for j in range(l):
            n = sum(sum(l[max(j-1, 0):j + 2]) for l in rows)
            if patt.data[i][j] == 0:
                new_p.data[i][j] = 1 if n == 3 else 0
            else:
                new_p.data[i][j] = 1 if n in (3, 4) else 0
    return new_p
