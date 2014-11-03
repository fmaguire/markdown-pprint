#!/usr/bin/env python

import sympy
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

        # interpret that expression with sympy
        # first have to define whatever symbols in there as variables
        varfd = re.compile(r'[a-z]', re.IGNORECASE)
        variables = varfd.findall(expression)

        # this line is complete hack
        ns = locals()

        code = compile('import sympy', '<string>', 'exec')
        exec(code, ns)

        code = compile(', '.join(
            variables) + ' = sympy.symbols("{0}")'.format(' '.join(
                variables)), '<string>', 'exec')
        exec(code, ns)

        code = compile('symeq = ' + expression, '<string>', 'exec')
        exec(code, ns)

        # then we can make the pretty string:
        prettystring = sympy.pretty(ns['symeq'])

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
