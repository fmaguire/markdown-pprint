#!/usr/bin/env python

import sympy
import re
import sys
import hashlib
from optparse import OptionParser


def main(fname, streaming=False, verbose=False):
    with open(fname) as mdfile:
        md = mdfile.read()
    # regex for finding sympy blocks 
    r = re.compile('<!---sympy(.*?)--->')
    # regex for finding what is on the next line
    nl = re.compile(r'\n(.*)\n')
    # regex for finding status information
    rst = re.compile('<!---status(.*?)--->')
    # regex for finding code blocks (hopefully with equations in them
    rcb = re.compile('.```(.*?)```..',re.DOTALL)
    # iterate, finding all equations and adding a pprint section after them

    position = 0
    eq = r.search(md[position:])

    while eq is not None:
        # update current position
        position = position + eq.end()
        # reset flags
        regenflag = True

        # extract the sympy expression
        expression = eq.groups()[0]

        # hash current equation    
        h = hashlib.md5(expression.encode('utf-8'))

        # check the next line for status information
        nextline = nl.search(md[position:])
        status = rst.search(nextline.group())

        if status:
            statuscontent = status.group().split(' ')
            statushash = statuscontent[1]
            # check status against current equation
            if h.hexdigest() == statushash:
                regenflag = False
            else:

                # equation must be changed, so remove the equation
                codeblock = rcb.search(md[position:])
                md = md[:position+codeblock.start()] + md[position+codeblock.end():]
                # status must also be overwritten, so remove that as well
                md = md[:position+status.start()] + md[position+status.end():]
                # update hash
                statuscontent[1] = h.hexdigest()
        else:
            # create status
            statuscontent = ["<!---status",h.hexdigest(),"--->"]

        if verbose:
            print('found equation {0} at position {1}'.format(expression,
                                                              position))
        # regenerate if flag is set:
        if regenflag:
            # add statuscontent to md
            statuscontent = ' '.join(statuscontent)
            md = md[:position] + '\n' + statuscontent \
                        + md[position:]

            # update position
            position = position + len(statuscontent) +1

            # parse string as sympy expression
            # might be worth adding a local dict of symbols too
            symeq_obj = sympy.sympify(expression)

            # then we can make the pretty string:
            prettystring = sympy.pretty(symeq_obj)

            md = md[:position] + '\n```\n' + prettystring \
                    + '\n```\n' + md[position:]

            if streaming is False:
                # writing this to the file in the right place
                with open(fname, 'w') as mdfile:
                    mdfile.write(md)

        # search again from new position
        eq = r.search(md[position:])

    if streaming is True:
        sys.stdout.write(md)

    return None

if __name__ == '__main__':

    parser = OptionParser()

    parser.add_option("-v", "--verbose",
                      action="store_true",
                      dest="verbose",
                      default=False,
                      help="Print verbose status during processing"
                           " (default=False)")

    parser.add_option("-s", "--stream",
                      action="store_true",
                      dest="streaming",
                      default=False,
                      help="Run markdownpp in streaming mode"
                           " (default=False)")


    (opts, args) = parser.parse_args()

    main(args[0], streaming=opts.streaming, verbose=opts.verbose)
