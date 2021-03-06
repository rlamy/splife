import attr

def char2state(c):
    if c == '.':
        return 0
    elif c == 'O':
        return 1
    else:
        raise ValueError("Invalid character '{c}'")

@attr.s
class Motif:
    """
    An array of cells
    """
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
        return Motif([[0] * width for _ in range(height)])

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

    def copy(self):
        return Motif([row[:] for row in self.data])

def successor(motif):
    h = motif.height
    l = motif.width
    new_p = Motif.empty(h, l)
    for i in range(h):
        rows = motif.data[max(i - 1, 0):i + 2]
        for j in range(l):
            n = sum(sum(l[max(j-1, 0):j + 2]) for l in rows)
            if motif.data[i][j] == 0:
                new_p.data[i][j] = 1 if n == 3 else 0
            else:
                new_p.data[i][j] = 1 if n in (3, 4) else 0
    return new_p

@attr.s
class Pattern:
    """
    A finite board configuration
    """
    cells = attr.ib()
    xmin = attr.ib()
    ymin = attr.ib()
    time = attr.ib(default=0)
    def canonicalize(self):
        if any(row[0] == 1 for row in self.cells.data):
            for row in self.cells.data:
                row.insert(0, 0)
            self.xmin -= 1
        if any(row[-1] == 1 for row in self.cells.data):
            for row in self.cells.data:
                row.append(0)
        if any(s == 1 for s in self.cells.data[0]):
            self.cells.data.insert(0, [0] * self.cells.width)
            self.ymin -= 1
        if any(s == 1 for s in self.cells.data[-1]):
            self.cells.data.append([0] * self.cells.width)

    def copy(self):
        return Pattern(self.cells.copy(), self.xmin, self.ymin, self.time)

    def step(self):
        self.canonicalize()
        self.cells = successor(self.cells)
        self.time += 1
