from __future__ import annotations

import re
import operator as op
from collections import UserDict
from typing import Optional

from ..opcode_compile.blocks import Block

STR_RE = re.compile(r'"((?:[^"\\]|\\.)*?)"')
IDENT_RE = re.compile(r'([a-zA-Z_]\w*)')
LIST_IDENT_RE = re.compile(r'[a-zA-Z_$][\w$]*')
LISTITEM_RE = re.compile(r'([a-zA-Z_$][\w$]*)'
                         r'\.'
                         r'([0-9]*|last|random|all)')
# just for reference, this isn't used anywhere
STR_REPL_RE = re.compile(r'!\*\$str:(\d+)\*!')


class AttrDict(UserDict):
    def __init__(self, obj: object):
        super().__init__(obj.__dict__)


class ContentReplacer:
    prefix = '!*${name}:'
    suffix = '*!'

    def __init__(self, name, value_pat: str = r'(\d+)'):
        self.name = name
        self.value_pat = value_pat
        self.inst_prefix = self.prefix.format(name=self.name)
        self.inst_suffix = self.suffix.format()
        self.pat = (re.escape(self.inst_prefix)
                    + self.value_pat
                    + re.escape(self.inst_suffix))
        self.re = re.compile(self.pat)

    def match(self, s: str, full=False):
        return self.re.fullmatch(s) if full else self.re.match(s)

    def make(self, value):
        return self.inst_prefix + str(value) + self.inst_suffix


STR_REPL = ContentReplacer("str")
PAR_REPL = ContentReplacer("par")


class StrReplacer:
    repl = STR_REPL

    def __init__(self, s: str):
        self.orig = s
        self.new: Optional[str] = None
        self.strings: 'list[str]' = []

    def replace(self):
        self.new = STR_RE.sub(self.replacer, self.orig)
        return self

    def replacer(self, m: re.Match):
        contents = m[1]
        idx = len(self.strings)
        self.strings.append(contents)
        return self.repl.make(idx)


class ParenMatcher:
    paren_types = ['()', '[]', '{}']
    open_parens = {s[0]: s[1] for s in paren_types}
    close_parens = {s[1]: s[0] for s in paren_types}

    def __init__(self, s: str, sort_by: str = None, reverse=False):
        self.orig = s.rstrip()
        self.sort_by = sort_by
        self.reverse = reverse
        self.finished = False
        self.consumed_all = None

    def sort(self, by: str = None, reverse=False):
        self.sort_by = by
        self.reverse = reverse
        self._sort_output()
        return self

    def match(self, sort=None, reverse=False):
        if not self.finished:
            self._match()
        self.sort(sort, reverse)
        return self

    def _match(self):
        self.out: 'list[tuple[str, int, int]]' = []
        self.paren_stack = []
        self.i = 0
        while self.i < len(self.orig) and not self.finished:
            self._handle_next_char()
        if not self.finished:
            # reached end of input
            self.consumed_all = True
            self.finished = True
        self._sort_output()

    def _sort_output(self):
        # don't sort if unfinished
        if not self.finished or self.sort_by is None:
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
        if self.c not in self.open_parens and self.c not in self.close_parens:
            return
        if self.c in self.open_parens:
            self.paren_stack.append((self.c, self.i))
            return
        if len(self.paren_stack) == 0:
            self.finished = True
            self.consumed_all = False
            return
        tos = self.paren_stack.pop()
        tos_c, tos_i = tos
        expected = self.open_parens[tos_c]
        if self.c == expected:
            self.out.append((tos_c + self.c, tos_i, self.i))
            return
        raise ValueError(f"Unmatched paren: expected '{expected}', got '{self.c}'")


class ParenReplacer:
    def __init__(self, text: str, pm: ParenMatcher = None):
        self.text = text
        self.pm = pm
        if self.pm is None:
            self.pm = ParenMatcher(self.text)
        self.pm.match(sort='start')

    def replace(self):
        self._replace()
        return self

    def _replace(self):
        self.par_contents = []
        self.new = ''
        par_end = 0
        for i, (t, start, end) in enumerate(self.pm.out):
            if i == 0:
                continue
            if start <= par_end:
                continue
            self.new += (self.text[par_end + 1:start]
                         + PAR_REPL.make(len(self.par_contents)))
            self.par_contents.append((self.text[start:end + 1], start, end))
            par_end = end
        self.end = self.pm.out[0][2]


def parses(s: str):
    ...
    return Parser(s).parse()


class Parser:
    expr_str: str
    left: str
    line: str

    def __init__(self, s: str):
        self.src = s

    def parse(self):
        self._parse()
        return self

    def _parse(self):
        self.smts = []
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
        self.assign_sides = [s.strip() for s in self.line.split('=')]
        if len(self.assign_sides) < 2:
            return False
        if len(self.assign_sides) > 2:
            raise NotImplementedError("Multiple assignment has not been implemented yet")
        self.left, self.expr_str = self.assign_sides
        self._handle_left()
        self._handle_expr()
        self._set_assign_target(self.expr_res)
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

    def _handle_expr(self):
        self._gen_assign_target()

    def _gen_assign_target(self):
        if self.expr_str.startswith('!*'):  # todo use an unprintable character (eg. \x1a)
            self.expr_res = self._get_next_str()
            return
        if self._check_int_expr():
            return
        if self._check_float_expr():
            return
        if self.expr_str.startswith("@"):
            self._handle_raw_op()
        raise SyntaxError("Unknown expression")

    def _handle_raw_op(self):
        self.raw_op_str: str = self.expr_str[1:]  # remove '@' prefix
        self.raw_op_parts = [s.strip() for s in self.raw_op_str.split('(', 1)]
        if len(self.raw_op_parts) == 0 or not self.raw_op_parts[0]:
            raise SyntaxError("Raw operation requires name")
        if len(self.raw_op_parts) == 1:
            # no args, just name 
            self.expr_res = Block(self.raw_op_parts[0])
        self.raw_op_name, self.op_args_str = self.raw_op_parts
        self.op_args_str = '(' + self.op_args_str  # add on removed '('

    def _get_next_str(self):
        m = STR_REPL.match(self.expr_str)
        assert m
        idx = int(m.group(1))
        s = _unescape(self.str_repl.strings[idx])
        return s

    def _check_int_expr(self):
        if self._try_convert_into_res(int, self.expr_str):
            return True
        if self._try_convert_with_base(self.expr_str, 2, "0b"):
            return True
        if self._try_convert_with_base(self.expr_str, 8, "0o"):
            return True
        if (self._try_convert_with_base(self.expr_str, 16, "0x")
                or self._try_convert_with_base(self.expr_str, 16, "0h")):
            return True

    def _try_convert_with_base(self, s: str, base: int, prefix: str):
        return s.startswith(prefix) and self._try_convert_into_res(int, s[2:], base)

    def _try_convert_into_res(self, converter, *args):
        try:
            self.expr_res = converter(*args)
            return True
        except ValueError:
            return None

    def _check_float_expr(self):
        return self._try_convert_into_res(float, self.expr_str)


def _unescape(s: str):
    # or encode with "latin-1", "backslashescape" ?
    return s.encode('raw_unicode_escape').decode('unicode_escape')


if __name__ == '__main__':
    import pprint

    test_text = "(some, (stuff), (), (other, things, (inner, ())))"
    pprint.pp(ParenReplacer(test_text).replace(), indent=2)
