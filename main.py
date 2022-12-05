import sys

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
            print("result:  ", self.actual, file=sys.stderr)
            raise TestFailed("Test failed")


expect = _Expect

PARSER_TESTS = [
    (
        'a =0x9b \n$y.12=  "ab\\x64\\"" \n   some="b\\\\x"\n  $ls.42 = 0b10101',
        [["setVar:to:", "a", 0x9b],
         ["setLine:ofList:to:", 12, "$y", 'abd"'],
         ['setVar:to:', 'some', 'b\\x'],
         ['setLine:ofList:to:', 42, '$ls', 0b10101]
         ]
    ),
    (
        'some  = @+(0o27, @-(0x3b, 0b11))\n   @deleteLine:ofList:(@/(18, 0h2), "ls")',
        [["setVar:to:", "some", ["+", 0o27, ["-", 0x3b, 0b11]]],
         ["deleteLine:ofList:", ["/", 18, 0x2], "ls"]]
    ),
    (
        '  value = 23 + 8\n $ls.7= 12+6-3-1+2\n\n@deleteLine:ofList:(3+@/(1-(9+7), 2))',
        [["setVar:to:", "value", ["+", 23, 8]],
         ["setLine:ofList:to:", 7, "$ls", ['+', ['-', ['-', ['+', 12, 6], 3], 1], 2]],
         ['deleteLine:ofList:', ['+', 3, ['/', ['-', 1, ['+', 9, 7]], 2]]]]
    )
]


def test():
    for i, (s, out) in enumerate(PARSER_TESTS):
        try:
            expect(parse(s)).to_be(out)
        except TestFailed:
            raise
        except Exception:
            print(f"Error occurred in test {i}:", file=sys.stderr)
            raise


test()
