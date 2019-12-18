#!/usr/bin/env python3

"""Main."""

import sys
filename = sys.argv[1]
from cpu import *

cpu = CPU(filename)

cpu.load()
cpu.run()
