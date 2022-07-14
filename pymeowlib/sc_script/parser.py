from __future__ import annotations

import re
from enum import auto, Enum
import operator as op
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


class ParenMatcher:
    paren_types = ['()', '[]', '{}']
    open_parens = {s[0]: s[1] for s in paren_types}
    close_parens = {s[1]: s[0] for s in paren_types}
    
    def __init__(self, s: str, sort_by: str = None, reverse=False):
        self.orig = s
        self.sort_by = sort_by
        self.reverse = reverse

    def match(self):
        self._match()
        return self

    def _match(self):
        self.out = []
        self.paren_stack = []
        self.i = 0
        while self.i < len(self.orig):
            self._handle_next_char()
        self._sort_output()

    def _sort_output(self):
        if self.sort_by is None:
            return
        if self.sort_by == 'type':
            self.sort_idx = 0
        if self.sort_by == 'start':
            self.sort_idx = 1
        if self.sort_by == 'end':
            self.sort_idx = 2
        self.out.sort(key=op.itemgetter(self.sort_idx), reverse=self.reverse)

    def _handle_next_char(self):
        self.c = self.orig[self.i]
        self._handle_char()
        self.i += 1
    
    def _handle_char(self):
        if self.c in self.open_parens:
            self.paren_stack.append((self.c, self.i))
            return
        if self.c in self.close_parens:
            tos = self.paren_stack.pop()
            tos_c, tos_i = tos
            expected = self.open_parens[tos_c]
            if self.c == expected:
                self.out.append((tos_c + self.c, tos_i, self.i))
                return
            raise ValueError(f"Unmatched paren: expected '{expected}', got '{self.c}'")
            

def parses(s: str):
    ...
    return Parser(s).parse()


class Parser:
    right: str
    left: str
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
        if not self.line:
            return
        self._handle_assign()
        self.smts.append(self.smt)

    def _handle_assign(self):
        self.assign_sides = map(str.strip, self.line.split('='))
        if len(self.assign_sides) < 2:
            return False
        if len(self.assign_sides) > 2:
            raise NotImplementedError("Multiple assignment has not been implemented yet")
        self.left, self.right = self.assign_sides
        self._handle_left()
        self._handle_right()
        return True

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
        if self._check_int_rvalue():
            return
        if self._check_float_rvalue():
            return
        if self.right.startswith("@"):
            self._handle_raw_op()
        raise SyntaxError("Unknown rvalue")

    def _handle_raw_op(self):
        self.raw_op_str: str = self.right[1:]  # remove '@' prefix
        self.raw_op_parts = map(str.split, self.raw_op_str.split('(', 1))
        if len(self.raw_op_parts) == 0 or not self.raw_op_parts[0]:
            raise SyntaxError("Raw operation requires name")
        if len(self.raw_op_parts) == 1:
            # no args, just name 
            self.target = Block(self.raw_op_parts[0])
        assert len(self.raw_op_parts) == 2
        ...
        # self.pmatcher = ParenMatcher(self.raw_op_str, 'start').match()
        # assert self.pmatcher.out[0][:2] == ('()', 0)
        

    def _get_next_str(self, inc=True):
        s = _unescape(self.str_repl.strings[self.str_index])
        if inc:
            self.str_index += 1
        return s

    def _check_int_rvalue(self):
        if self._try_convert_to_target(int, self.right):
            return True
        if self._try_convert_with_base(self.right, 2, "0b"):
            return True
        if self._try_convert_with_base(self.right, 8, "0o"):
            return True
        if (self._try_convert_with_base(self.right, 16, "0x")
                or self._try_convert_with_base(self.right, 16, "0h")):
            return True

    def _try_convert_with_base(self, s: str, base: int, prefix: str):
        return s.startswith(prefix) and self._try_convert_to_target(int, s[2:], base)

    def _try_convert_to_target(self, converter, *args):
        try:
            self.target = converter(*args)
            return True
        except ValueError:
            pass

    def _check_float_rvalue(self):
        return self._try_convert_to_target(float, self.right)


def _unescape(s: str):
    # or encode with "latin-1", "backslashescape" ?
    return s.encode('raw_unicode_escape').decode('unicode_escape')
