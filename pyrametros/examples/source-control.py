#!/usr/bin/python
"""Fills opcodes in scavenger-opcm.h"""

import sys
sys.path.append("../../")

from Pyrametros.cfile import CFile
from Pyrametros.parser import Row, parse_file

# Parse the table
grid = parse_file('testtable.txt')

# Open a file to edit
f = CFile('scavenger-opcm.h', 'instruction names')

for i in grid[1:]:
    # Create dictionary style rows. Note that numbers are striped from header keys.
    dictionary = Row(grid[0],i)

    # Put a line in the file
    f.push_line(dictionary['opcode']+",\n")

# Dont forget to flush
f.flush()