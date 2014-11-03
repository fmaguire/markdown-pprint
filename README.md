markdown-pprint
===============

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
