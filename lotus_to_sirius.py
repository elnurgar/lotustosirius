#!/usr/bin/env python
# coding: utf-8

# In[34]:


# A simple script to convert lotus results into sirius db input

INPUT_FILE = "lotus.sdf"
OUTPUT_FILE = "lotus.csv"

with open(INPUT_FILE, 'r+') as f:
    x = f.read()
    x = x.replace("> <lotus_id> \n", "LOTUSID")
    x = x.replace("> <SMILES> \n", "SMILES")
    f.seek(0)
    f.write(x)

class Entry:
    name = ""
    inchi = ""
    LINE_MODE = False
    def __init__(self):
        self.lines = []
    def add_lines_from_line(self, text_line):
        split_line = text_line.split(" ")
        for i in range(0, len(split_line), 2):
             self.lines+=[[split_line[i], split_line[i+1]]]

entries = []

with open(INPUT_FILE, "r") as f:
    entry = Entry()
    for line in f:
        line_s = line.strip()
        if line_s == "$$$$":
            entries += [entry]
            entry = Entry()
        elif entry.LINE_MODE:
            entry.add_lines_from_line(line_s)
        elif line_s.startswith("LOTUSID"):
            entry.name = line_s[7:]
        elif line_s.startswith("SMILES"):
            entry.inchi = line_s[6:]
print(f"Found {len(entries)} entries.")


# In[35]:


with open(OUTPUT_FILE, "w") as f:
    for entry in entries:
        f.write(f"{entry.inchi}\t")
        f.write(f"{entry.name}\n")
        for line in entry.lines:
            f.write(f"{line[0]} {line[1]}\n")


