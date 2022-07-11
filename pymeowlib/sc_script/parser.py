from __future__ import annotations

import re
from typing import Optional

from ..opcode_compile.blocks import Block

STR_RE = re.compile(r'"((?:[^"\\]|\\.)*?)"')
IDENT_RE = re.compile(r'([a-zA-Z_]\w*)')
LIST_IDENT_RE = re.compile(r'[a-zA-Z_$][\w$]*')
LISTITEM_RE = re.compile(r'([a-zA-Z_$][\w$]*)'
                         r'\.'
                         r'([0-9]*|last|random|all)')


class StrReplacer:
    def __init__(self, s: str):
        self.orig = s
        self.new: Optional[str] = None
        self.strings: 'list[str]' = []

    def replace(self):
        self.new = STR_RE.sub(self.replacer, self.orig)
        return self

    def replacer(self, m: re.Match):
        contents = m[1]
        self.strings.append(contents)
        return '!*'


def parses(s: str):
    ...
    return Parser(s).parse()


class Parser:
    line: str

    def __init__(self, s: str):
        self.src = s

    def parse(self):
        self._parse()
        return self

    def _parse(self):
        self.smts = []
        self.str_index = 0
        self.str_repl = StrReplacer(self.src).replace()
        if self.str_repl.new.count('!*') != len(self.str_repl.strings):
            raise SyntaxError("Invalid syntax: !* may not be used outside of strings")
        for self.line in self.str_repl.new.splitlines():
            self._handle_line()

    def _handle_line(self):
        self.smt: Optional[Block] = None
        self.line = self.line.strip()
        self.left, self.right = map(str.strip, self.line.split('='))
        self._handle_left()
        self._handle_right()
        self.smts.append(self.smt)

    def _handle_left(self):
        if self._check_var_assign():
            self._init_var_assign()
            return
        if self._check_listitem_assign():
            self._init_listitem_assign()
            return
        raise SyntaxError("Invalid LHS of assignment")

    def _check_var_assign(self):
        m = IDENT_RE.fullmatch(self.left)
        if m:
            self.assign_type = 'var'
            self.ident = m[1]
            return True

    def _init_var_assign(self):
        self.smt = Block("setVar:to:", self.ident, None)

    def _check_listitem_assign(self):
        m = LISTITEM_RE.fullmatch(self.left)
        if m:
            self.assign_type = 'list'
            self.ident, self.index = m[1], m[2]
            return True

    def _init_listitem_assign(self):
        self.smt = Block("setLine:ofList:to:", int(self.index), self.ident, None)

    def _set_assign_target(self, target):
        if self.assign_type == 'var':
            self.smt.data[2] = target
        elif self.assign_type == 'list':
            self.smt.data[3] = target
        else:
            assert False

    def _handle_right(self):
        self._gen_assign_target()
        self._set_assign_target(self.target)

    def _gen_assign_target(self):
        if self.right == '!*':
            self.target = self._get_next_str()
            return
        try:
            self.target = int(self.right)
            return
        except ValueError:
            pass
        try:
            self.target = float(self.right)
            return
        except ValueError:
            pass
        raise SyntaxError("Unknown rvalue")

    def _get_next_str(self, inc=True):
        s = _unescape(self.str_repl.strings[self.str_index])
        if inc:
            self.str_index += 1
        return s


def _unescape(s: str):
    return s.encode('raw_unicode_escape').decode('unicode_escape')
