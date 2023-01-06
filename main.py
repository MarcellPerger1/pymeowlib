from __future__ import annotations

import inspect
import sys
from typing import Any

import pymeowlib
import pymeowlib.sc_script.parser


def parse(s):
    return [smt.get_data() for smt in pymeowlib.sc_script.parser.parses(s).smts]


class TestFailed(AssertionError):
    ...


class _Expect:
    expected: object

    def __init__(self, o: object):
        self.actual = o

    def to_be(self, expected: object):
        self.expected = expected
        if self.expected != self.actual:
            print("expected:", self.expected, file=sys.stderr)
            print("result:  ", self.actual, file=sys.stderr, end="\n\n")
            raise TestFailed("Test failed")


expect = _Expect


class _ParserTestCase:
    expected: Any
    want_error: Any

    def __init__(self, name: str = None, inp: str = None, result=None, want_error=None):
        self.inp = inp
        self.name = name
        if result is None:
            return
        if want_error is None:
            want_error = isinstance(result, Exception) or issubclass(result, Exception)
        if want_error:
            self.error(result)
        else:
            self.result(result)

    def input(self, inp: str):
        self.inp = inp
        return self

    def result(self, result):
        self.expected = result
        self.want_error = False
        return self

    def error(self, e: Exception | type[Exception]):
        self.expected = e
        self.want_error = True
        return self

    def with_name(self, name: str):
        self.name = name

    def run_normal(self, i: int):
        inp = self.inp
        name = repr(self.name) if self.name is not None else f'test {i}'
        try:
            expect(parse(inp)).to_be(self.expected)
        except TestFailed:
            raise
        except Exception:
            print(f"Error occurred in {name} (and wasn't expecting error):",
                  file=sys.stderr, end="\n\n")
            raise

    def run_errors(self, i: int):
        inp = self.inp
        name = repr(self.name) if self.name is None else f'test {i}'
        is_cls = inspect.isclass(self.expected)
        expected_t = self.expected if is_cls else type(self.expected)
        try:
            result = parse(inp)
        except expected_t as e:
            e: Exception
            if is_cls:
                return
            if e.args == self.expected.args:
                return
            if len(e.args) == 1 and len(self.expected.args) == 1:
                if self.expected.args[0] not in e.args[0]:
                    print(f"Unexpected error occurred in {name}; "
                          f"was expecting args containing "
                          f"{self.expected.args[0]!r}, got args {e.args[0]!r}",
                          file=sys.stderr, end="\n\n")
                return
            print(f"Unexpected error occurred in {name}; "
                  f"was expecting args {self.expected.args}, got args {e.args!r}",
                  file=sys.stderr, end="\n\n")
            raise
        except Exception as e:
            print(f"Unexpected error occurred in {name}; "
                  f"was expecting {self.expected}, got {e!r}",
                  file=sys.stderr, end="\n\n")
            raise
        else:
            raise TestFailed(f"Was expecting error in {name} but got no error;"
                             f" return value was {result}")

    def run(self, i: int):
        if self.want_error:
            self.run_errors(i)
        else:
            self.run_normal(i)


ptest = _ParserTestCase

PARSER_TESTS = [
    ptest("Test basic assignment")
    .input('a =0x9b \n$y.12=  "ab\\x64\\"" \n   some="b\\\\x"\n  $ls.42 = 0b10101')
    .result(
        [["setVar:to:", "a", 0x9b],
         ["setLine:ofList:to:", 12, "$y", 'abd"'],
         ['setVar:to:', 'some', 'b\\x'],
         ['setLine:ofList:to:', 42, '$ls', 0b10101]
         ]
    ),
    ptest('Test raw operations')
    .input('some  = @+(0o27, @-(0x3b, 0b11))\n   @deleteLine:ofList:(@/(18, 0h2), "ls")')
    .result(
        [["setVar:to:", "some", ["+", 0o27, ["-", 0x3b, 0b11]]],
         ["deleteLine:ofList:", ["/", 18, 0x2], "ls"]]
    ),
    ptest('Test + and -')
    .input('  value = 23 + 8\n $ls.7= 12+6-3-1+2\n\n@deleteLine:ofList:(3+@/(1-(9+7), 2))')
    .result(
        [["setVar:to:", "value", ["+", 23, 8]],
         ["setLine:ofList:to:", 7, "$ls", ['+', ['-', ['-', ['+', 12, 6], 3], 1], 2]],
         ['deleteLine:ofList:', ['+', 3, ['/', ['-', 1, ['+', 9, 7]], 2]]]]
    ),
    ptest('Test all operators')
    .input('$q.10 = 11 * 8 / (3+2*7) / 2 * 7 - 8 / @rounded(12.8 + 2*7.2) - 3')
    .result(
        [["setLine:ofList:to:", 10, "$q", [
            "-", [
                "-", [
                    "*", [
                        "/", [
                            "/", ["*", 11, 8], ["+", 3, ["*", 2, 7]]
                        ], 2],
                    7],
                ["/", 8, ["rounded", [
                    "+", 12.8, ["*", 2, 7.2]
                ]]]
            ], 3
        ]]]
    )
]
PARSER_TESTS += [
    ptest('Tests invalid LHS')
    .input('3 = 4')
    .error(SyntaxError("Invalid LHS of assignment")),
    ptest('Test invalid list LHS')
    .input('$w.7o = 4')
    .error(SyntaxError("Invalid LHS of assignment")),
    ptest('No extra tokens after raw op')
    .input('@rounded(2.2) 123')
    .error(SyntaxError("Unexpected extra tokens after raw op"))
]


def test():
    for i, v in enumerate(PARSER_TESTS):
        if isinstance(v, _ParserTestCase):
            v.run(i)
            continue
        s, out = v
        try:
            expect(parse(s)).to_be(out)
        except TestFailed:
            raise
        except Exception:
            print(f"Error occurred in test {i}:", file=sys.stderr)
            raise


test()
