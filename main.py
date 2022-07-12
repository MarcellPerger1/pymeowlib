# noinspection PyUnresolvedReferences
import pymeowlib
import pymeowlib.sc_script.parser

def parse(s):
    return [smt.get_data() for smt in pymeowlib.sc_script.parser.parses(s).smts]

