import sys
import struct

class Glyph:
    def __init__(self, file, offset):
        self.beg_x = 0
        self.beg_y = 0
        self.len_x = 0
        self.len_y = 0
        self.width = 0
        self.data = None
        self.file = file
        self.file.seek(offset)

    def read(self):
        # Read the glyph header
        self.beg_x, self.beg_y, self.len_x, self.len_y = self.file.read(4)

        # Compute the size to read including the last byte
        size = self.len_x * self.len_y
        size = (size + 7) // 8

        # Optimization: do not split the row/columns yet
        self.data = self.file.read(size)

        # Get the ceiling with a granularity of 32
        self.width = self.len_x + 32 - ((self.len_x - 1) % 32 + 1)

class Font:
    def __init__(self, path):
        self.file = open(path, "rb")

        # Read the index header: (u32)*2
        record = self.file.read(4 + 4)
        self.height, self.index_size = struct.unpack(">II", record)

        # Then read the index
        self.index = []
        n = 0
        while n < self.index_size:
            # Parse a record from the file
            self.index.append(struct.unpack(">II", self.file.read(8)))
            n += 8
            x = self.index[len(self.index) - 1]

    def glyph_range(self, unicode):
        # Start searching from the middle of the file
        beg = 0
        end = len(self.index)
        i = beg + (end - beg) // 2

        # Inline implementation of binary search to find the glyph
        while beg != end:

            # Decode the u8 and u24 out of the u32
            unicode_len = self.index[i][0] & 0xff
            unicode_start = self.index[i][0] >> 8

            # Should we search lower?
            if unicode < unicode_start:
                end = i

            # Should we search higher?
            elif unicode > unicode_start + unicode_len:
                beg = i + 1

            # That's a hit!
            else:
                return unicode_start, self.index[i][1]

            # Adjust the probe
            i = beg + (end - beg) // 2

        raise ValueError("glyph not found in font")

    def glyph(self, unicode):

        # Get the range to start scanning from
        range_start, range_address = self.glyph_range(unicode)

        # Scan through the data glyph per glyph
        glyph = Glyph(self.file, 4 + 4 + self.index_size + range_address)

        # Skip several glyphs until we are there
        for _ in range(unicode - range_start):
            glyph.read()
        glyph.read()

        return glyph

    def render(self, glyph, bg=b" ", fg=b"#"):
        n = 0
        canvas = bytearray()

        # Fill empty area above the glyph
        canvas.extend(bg * glyph.beg_y * glyph.width)

        # Fill the glyph content
        for ch in glyph.data:
            for i in reversed(range(8)):

                # Pad with background at the right
                if n % glyph.len_x == 0:
                    canvas.extend((glyph.width - glyph.len_x) * bg)

                # Fill with foreground or background according to the data
                canvas.extend(fg if ch & (1 << i) else bg)
                n += 1

        # Fill the rest of the line if needed
        while len(canvas) % glyph.width != 0:
            canvas.extend(bg)

        empty_rows = max(self.height - glyph.len_y - glyph.beg_y, 0)
        canvas.extend(bg * empty_rows * glyph.width)

        return canvas
