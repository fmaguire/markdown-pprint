#!/usr/bin/env python

import sympy
import sympy.parsing.sympy_parser as sp
import re
from optparse import OptionParser


def main(fname, verbose=False):
    with open(fname) as mdfile:
        md = mdfile.read()

    r = re.compile('<!---sympy(.*)--->')
    # iterate, finding all equations and adding a pprint section after them

    position = 0
    eq = r.search(md[position:])

    while eq is not None:
        # update current position
        position = position + eq.end()

        # extract the sympy expression
        expression = eq.groups()[0]

        if verbose:
            print('found equation {0} at position {1}'.format(expression,
                                                              position))

        # parse string as sympy expression
        # might be worth adding a local dict of symbols to
        # parse_expr
        symeq_obj = sp.parse_expr(expression)

        # then we can make the pretty string:
        prettystring = sympy.pretty(symeq_obj)

        # writing this to the file in the right place
        with open(fname, 'w') as mdfile:
            md = md[:position] + '\n```\n' + prettystring \
                + '\n```\n' + md[position:]

            mdfile.write(md)

        # search again from new position
        eq = r.search(md[position:])

    return None

if __name__ == '__main__':

    parser = OptionParser()

    parser.add_option("-v", "--verbose",
                      action="store_true",
                      dest="verbose",
                      default=False,
                      help="Print verbose status during processing"
                           " (default=False)")

    (opts, args) = parser.parse_args()

    main(args[0], verbose=opts.verbose)
