markdown-pprint
===============

[![Build Status](https://travis-ci.org/fmaguire/markdown-pprint.svg?branch=master)](https://travis-ci.org/fmaguire/markdown-pprint)

A pretty printer for equations in markdown where MathJax isn't supported, such as on the github wiki pages.
Uses Sympy so math commands have to be in Sympy style in the following way:

```
<!---sympy x**2 - (x+3)/2 --->
```

Which will produce:

<!---sympy x**2 - (x+3)/2 --->
```
 2   x   3
x  - ─ - ─
     2   2
```

Similarly, this:

```
<!---sympy x**2 - (a+3)/2 --->
```

Produces:

<!---sympy x**2 - (a+3)/2 --->
```
  a    2   3
- ─ + x  - ─
  2        2
```

Can also work with equations, but the equals sign isn't supported.
If you want to write an equations you have to use the `Eq(left,right)` expression:

```
<!---sympy Eq(H(X,Y),Sum(P(x,y)*log(1/P(x,y)),(x,a_X,A_X),(y,a_Y,A_Y))) --->
```

Produces:

<!---sympy Eq(H(X,Y),Sum(P(x,y)*log(1/P(x,y)),(x,a_X,A_X),(y,a_Y,A_Y))) --->
```
            A_Y     A_X                       
            ____    ____                      
            ╲       ╲                         
             ╲       ╲               ⎛   1   ⎞
              ╲       ╲   P(x, y)⋅log⎜───────⎟
H(X, Y) =     ╱       ╱              ⎝P(x, y)⎠
             ╱       ╱                        
            ╱       ╱                         
            ‾‾‾‾    ‾‾‾‾                      
          y = a_Y x = a_X                     
```

Which illustrates a couple of problems with subscript and the sum notation being crude at the moment.

This doesn't do anything clever and is only designed to be run only in batch at the moment.
It will, for example, generate double equations if you run it over a file twice.

I would have preferred it parse stand markdown latex syntax, but it was more difficult to parse that into sympy for the pretty printer.
It looks like [there are ways to do this][stack], but I haven't figured out an easy way to implement them here yet.

[stack]: https://stackoverflow.com/questions/15805882/convert-a-latex-formula-to-a-type-that-can-be-used-inside-sympy

Usage
-----

This works on the command line as long as you have Python 3 and Sympy installed:

```
./markdownpprint <filename.md>
```

You can also get verbose output on what equations are being processed by using -v:

```
./markdownpprint -v <filename.md>
```

Or run the program in streaming mode which sends output to stdout and doesn't modify the input file:

```
./mardownpprint -s <filename.md>
```

Unit tests can be run by invoking the following in the main directory:

```
./test/test.py
```
