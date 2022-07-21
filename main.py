# noinspection PyUnresolvedReferences
import pymeowlib
import pymeowlib.sc_script.parser


def parse(s):
    return [smt.get_data() for smt in pymeowlib.sc_script.parser.parses(s).smts]


def test():
    import sys
    s = 'a =0x9b \n$y.12=  "ab\\x64\\"" \n   some="b\\\\x"\n  $ls.42 = 0b10101'
    expected = [
        ["setVar:to:", "a", 0x9b],
        ["setLine:ofList:to:", 12, "$y", 'abd"'],
        ['setVar:to:', 'some', 'b\\x'],
        ['setLine:ofList:to:', 42, '$ls', 0b10101]
    ]
    result = parse(s)
    if result != expected:
        print("expected:", expected, file=sys.stderr)
        print("result:  ", result, file=sys.stderr)
        raise AssertionError("Test failed")


test()
