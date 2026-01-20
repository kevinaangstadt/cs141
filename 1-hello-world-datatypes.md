# Hello World and Types of Data in MicroPython

## Hello World
[MicroPython](https://micropython.org/) is a programming language for
microcontrollers that is based on [Python](https://python.org), a popular
programming language used widely in industry and academia. Python is used for
everything from web programming, scientific computing, data science, to
developing games. It is a powerful general purpose programming language and is
often used in introductory programming courses because it is relatively easy to
learn and get started with.

MicroPython provides a lean and efficient implementation of Python that is small
enough to run on microcontrollers. It allows the same ease of development as
Python while providing access to low-level hardware features of
microcontrollers.

Let's get started!

It is almost obligatory that [Hello
World](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program) be the first
program one writes in any programming language. Here is our first Python
program:

```{code-block} python
:linenos:
print("Hello, World!")
```

That is it, just the one line. And it does as you might expect, it prints the
message `Hello, World!` on the {term}`console`. But there is a lot going on in
that one line, so lets break it down.

:::{note} 
The *console* is a text window where Python sends the output of `print`
statements and where the user can also enter data from `input` statements. 
::: 

## Anatomy of Hello World
The line of code above, in its entirety, is called a {term}`statement`. A
statement is a complete instruction that tells the computer to do something.

The {term}`built-in function` `print` prints, to the console, the values between
the parentheses. Functions are an idea that is borrowed from mathematics. In general:

- A function transforms data in some way
- We give the function some input data (called {term}`arguments <argument>`)
  between the parentheses
- The function *returns* or produces some data that we can use later in our program

:::{note}

In mathematics, a *function* maps values in a *domain* to values in a *range*.
For example, the function $f(x) = x^2$ maps the input 2 to the output 4, 3 to
9, 1.5, to 2.25, etc.

:::

 In the case of Hello World, the value being provided to the `print` function is
the {term}`string literal` `"Hello, World!"`. A string literal in MicroPython is
a sequence of characters between double quotes or single quotes. More on string
literals later. The associated data created by this string literal is often
called a string {term}`constant` because the value does not change during the
execution of a program.

The `print` function can take any number of arguments, separated by commas. It will print these values to the console, separated by spaces. For example:

```{code-block} python
:linenos:
print("Hello,", "World!", 123)
```

produces the output:
```
Hello, World! 123
```

:::{exercise}
:label: ex-pi-print-output
What is the output of the following code?

```{code-block} python
:linenos:
print("The value of pi is approximately", 3.14159)
```
:::

:::{solution} ex-pi-print-output
:class: dropdown
`The value of pi is approximately 3.14159`
:::

## Functions as Black Boxes

Pictorially we can think of a function as a black box (we may not know how it
works) where values come in (represented by the arrow coming in on the left) and
the function produces values (the return results represented by the arrow coming
out of the box on the right).

```{figure} ./img/function-fx.png
:label: fig-function-box
:alt: A function as a black box with input arguments and return values
:align: center
A function as a black box with input arguments and return values.
```

## Integer and Floating Point Data
Consider the following code:

```{code-block} python
:linenos:
print("The value of pi squared is", 3.14159 * 3.14159)
```

This produces:
```
The value of pi squared is 9.869587728099999
```

Here we see that the `print` function can take not only string literals as
arguments, but also numerical values and even perform arithmetic operations. We
can see right here that 

1. `*` is part of Python, 
2. that a value is on each side of the `*` (syntax), and 
3.  that `*` must mean *multiplication* (semantics).

The second argument in the call to the `print` function above is the
mathematical expression `3.14159 * 3.14159`. In just about every programming
language the asterisk character `*` represents multiplication. A value such as
`3.14159` in mathematics is called a *real number* (a number with a decimal
point), but in programming languages we often refer to such numbers as
{term}`floating-point` numbers (or just *floats* for short).

There is a big difference between the string literal `"3.0"` and the
floating-point literal `3.0`.

:::{exercise}
:label: ex-string-vs-float
What would get printed by the following print statement?
```{code-block} python
:linenos:
print("3.0 * 3.0", 3.0 * 3.0)
```
:::

:::{solution} ex-string-vs-float
:class: dropdown
`3.0 * 3.0 9.0`
:::

Numbers without decimal points are called {term}`integers <integer>` or *ints*
for short.

### Integer and Floating Point Literals
Valid *integer literals* include numbers such as 0, 1, 2, ... and also negative
integers -1, -2, -3, ...

:::{warning}
Don't start an integer literal with a leading `0`, such as `09`. This is an error in Python.
:::

Floating-point literals include a decimal place, and include numbers such as
`0.3`, `-0.3`, `.3`, `3.`, `-3.14159`.

Python (as do most programming languages) supports specifying numbers using
*scientific notation*. For example, in Chemistry and Physics, Avogadro's number
is $6.022140857 \times 10^{23}$. Writing this out as
`602214085700000000000000` is not very readable. In Python, we can instead write
Avogadro's number as `6.022140857e23`.

:::{note}
Typically if we use scientific notation we write the number so that there is one 
non-zero digit to the left of the decimal point.  In this case we say that the 
number is *normalized*.
:::

We can also use scientific notation for very small numbers.  The mass of an
electron is $9.10938356 \times 10^{-31}$ kg.  Again, writing this as
`0.000000000000000000000000000000910938356` is not helpful. We should instead
write `9.10938356e-31`.

:::{exercise}
:label: ex-scientific-notation
The radius of an electron is *0.00000000000000281792* meters. Express this number using Python's scientific notation.
:::
:::{solution} ex-scientific-notation
:class: dropdown
`2.81792e-15` meters
:::

## Variables
Let's return to our simple program. Consider the following modification:

```{code-block} python
:linenos:
print("The value of pi squared is", 3.14159 * 3.14159)
```

It would be convenient to give the value `3.14159` a name. An obvious choice
being `pi`.  We do that in Python by defining a {term}`variable` using an
*assignment statement*.

```{code-block} python
:linenos:
pi = 3.14159
print("The value of pi squared is", pi * pi)
```

To the left of the `=` sign is a *variable name* and we read the assignment
statement above as `pi` *gets the value of* the value on the right of `=`, in
this case `3.14159`. Or simply, "pi is assigned 3.14159".

Variable names in Python should be meaningful. We could have said
```{code-block} python
:linenos:
dingbob = 3.14159
print("The value of pi squared is", dingbob * dingbob)
```
but this makes the code less understandable.

Variable names must start with either an alphabetic character (a - z, A - Z) or
underscore, and may also contain digits. Variable names are also *case
sensitive*, so `pi`, `Pi`, and `PI` are all different variable
names.[^variable_names]

The value on the right of `=` can also be an *expression*.
:::{important}
Students often confuse `=` with mathematical equality and think `3.14159 = pi` is the same thing as `pi = 3.14159`. The former is not valid Python.
:::


```{code-block} python
:linenos:
pi = 3.14159
pi_squared = pi * pi
print("The value of pi squared is", pi_squared)
```

:::{important}
Variables must be defined before they are used.

The Python program 

```{code-block} python
:linenos:
print(x)
```

would produce an error because the variable `x` does not have a value.
:::

:::{important}
Variable names are not string literals.
:::

:::{exercise}
:label: ex-string-data-difference
What is the difference between the following two lines of code?
```{code-block} python
:linenos:
print("The value of pi squared is", pi_squared)    <1>
print("The value of pi squared is", "pi_squared")  <2>
```
:::
:::{solution} ex-string-data-difference
:class: dropdown
<1> prints `The value of pi squared is 9.869587728099999`, while
<2> prints `The value of pi squared is pi_squared`. 
Almost certainly not what was intended.
:::

## Comments
We can add notes to our program using a {term}`comment`. In Python a one line comment starts 
with a hashtag and continues to the end of the line.

```{code-block} python
:linenos:
# define a variable pi
pi = 3.14159
```

You can also use a comment to finish a line.

```{code-block} python
:linenos:
pi = 3.14159  # define a variable pi
```

## Arithmetic Expressions
The most common arithmetic operators we will be using are:

| Operator |     Meaning      | Example  |
| :------: | :--------------: | :------: |
|    +     |     Addition     | `2 + 3`  |
|    -     |   Subtraction    | `3 - 2`  |
|    *     |  Multiplication  | `2 * 3`  |
|    /     |    Divisition    | `3 / 2`  |
|    //    | Integer Division | `3 // 2` |
|    %     | Remainder (mod)  | `3 % 2`  |
|    **    |  Exponentiation  | `2 ** 3` |

MicroPython has many more operators than shown in this table, but this is all we
will need for now.  You can combine these operations in complicated ways
including using parentheses. The *normal order of operations* you learned in
grade school apply.

* parentheses
* exponentiation
* multiplication, division (include remainder)
* addition and subtraction


If there are two operators at the same precedence then they should be evaluated
from left to right. For example `4 - 5 + 3` should be evaluated as `(4 - 5) + 3`
(which is `2`) and not `4 - (5 + 3)` (which is `-4`).


[^variable_names]: In reality Python 3 is much more flexible on what characters can
    be used in variables names including Greek characters such as
    `α`,`β`,`γ`,`δ`,`Γ`,`Δ`. Maybe a better variable name than `pi` is `π`.