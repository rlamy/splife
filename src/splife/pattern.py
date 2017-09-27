import attr

def char2state(c):
    if c == '.':
        return 0
    elif c == 'O':
        return 1
    else:
        raise ValueError(f"Invalid character '{c}'")

@attr.s
class Pattern:
    data = attr.ib()

    def __eq__(self, other):
        return all(x == y for x, y in zip(self.data, other.data))

    @property
    def height(self):
        return len(self.data)

    @property
    def width(self):
        return len(self.data[0])

    @classmethod
    def empty(cls, height, width):
        return Pattern([[0] * width for _ in range(height)])

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

    def canonicalize(self):
        if any(row[0] == 1 for row in self.data):
            for row in self.data:
                row.insert(0, 0)
        if any(row[-1] == 1 for row in self.data):
            for row in self.data:
                row.append(0)
        if any(s == 1 for s in self.data[0]):
            self.data.insert(0, [0] * self.width)
        if any(s == 1 for s in self.data[-1]):
            self.data.append([0] * self.width)

def successor(patt):
    h = patt.height
    l = patt.width
    new_p = Pattern.empty(h, l)
    for i in range(h):
        rows = patt.data[max(i - 1, 0):i + 2]
        for j in range(l):
            n = sum(sum(l[max(j-1, 0):j + 2]) for l in rows)
            if patt.data[i][j] == 0:
                new_p.data[i][j] = 1 if n == 3 else 0
            else:
                new_p.data[i][j] = 1 if n in (3, 4) else 0
    return new_p
