#!/usr/bin/env python
#
# Copyright (c) 2014 Paul Sokolovsky
# This file is licensed under MIT license.
#
# "lztxt" is a simple text-based format to represent work (i.e. compression)
# results of LZ77 algorithms family. Format explicitly represents literal
# bytes and copies of substrings from the previous stream history, and thus
# can represent results of any LZ77-like compression algorithm, without
# added complexity of bytestream or bitstream encoding. Thus, this format
# can be used to learn and study LZ77 compressions methods, and validate
# compressors.
#
# Format spec:
#
# L<xx> - literal byte value encoded in hex
# C<offset>,<length> - substring copy at <offset> and size of <length>.
#       <offset> should be negative and counted from current position in
#       uncompressed stream (current position (yet to be decompressed) = 0,
#       last decompressed byte = -1, etc). Note that length be larger than
#       absolute value of offset, this is useful to encoded sequences
#       repeating multiple times (as a particular case, to encode RLE
#       (run-length encoding) with offset = -1). Copy thus should be
#       performed byte by byte, accessing bytes which could have been
#       in the previous iteration.
#
# Example:
#   Laa
#   L55
#   C-1,3
#
# Expands to:
#   aa 55 55 55 55

import sys


f = open(sys.argv[1])
buf = bytearray()

for l in f:
    l = l.rstrip()
    if not l or l[0] == "#":
        continue
    elif l[0] == "L":
        val = int(l[1:3], 16)
        buf.append(val)
    elif l[0] == "C":
        off, sz = [int(x) for x in l[1:].split(",")]
        for i in range(sz):
            buf.append(buf[off])

with open(sys.argv[2], "wb") as f:
    f.write(buf)
