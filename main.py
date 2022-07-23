# noinspection PyUnresolvedReferences
import sys

import pymeowlib
import pymeowlib.sc_script.parser


def parse(s):
    return [smt.get_data() for smt in pymeowlib.sc_script.parser.parses(s).smts]


class _Expect:
    expected: object

    def __init__(self, o: object):
        self.actual = o

    def to_be(self, expected: object):
        self.expected = expected
        if self.expected != self.actual:
            print("expected:", self.expected, file=sys.stderr)
            print("result:  ", self.actual, file=sys.stderr)
            raise AssertionError("Test failed")


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
        'some  = @+(0o27, @-(0x3b, 0b11))',
        [["setVar:to:", "some", ["+", 0o27, ["-", 0x3b, 0b11]]]]
    )
]


def test():
    for s, out in PARSER_TESTS:
        expect(parse(s)).to_be(out)


test()
