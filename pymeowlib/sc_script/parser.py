import re


STR_RE = re.compile(r'"((?:[^"\\]|\\"|\\\\|\\.)*)"')

def replacer(m):
    pass

def parses(s: str):
    for line in s.splitlines():
        line: str = line.strip()
        