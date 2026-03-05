# Conditionals and Randomness

In the previous chapters, we have seen how loops can help us repeat a block of
code multiple times. With each iteration of a loop, MicroPython evaluates a
condition to determine whether to continue looping or to stop. What if we only
wish to execute a block of code *once* if a certain condition is met? This is
where *conditional statements* come into play.

In this chapter, we will cover the basics of conditional statements in Python
using random numbers to demonstrate how they work.

## Random Numbers

Let's simulate tossing a coin and print `Heads` or `Tails` with a 50-50 chance.

The `random` module contains many functions for generating random numbers. The
function `random.random()` returns a `uniform` floating-point number between 0
and 1.

:::{note}
A random number generator is *uniform* if all outcomes are equally likely.
:::

```{code-block} python
:linenos:

import random
print(random.random())
```

```
0.2840077963246783
```

The function `random.randrange(n)` returns a *uniform* random integer between 0
and `n-1` inclusive. 

```{code-block} python
:linenos:

import random
print(random.randrange(6))
```

It is also possible to provide two arguments to `random.randrange(start, stop)` to get a random integer between `start` and `stop-1` inclusive.

```{code-block} python
:linenos:
import random
print(random.randrange(10, 20))
```

## If-Statements
We will need some way to check what the random number generator produced. An
*if-statement* executes one of two possible blocks of statements depending on a
logical condition.

```{code-block} python
:linenos:
if 〈condition〉:
    true_stmts
else:
    false_stmts
```

If the condition is `True` then the block of statements labeled `true_stmts`
will be executed, otherwise the block of statements labeled `false_stmts` will
be executed. The `else` part is optional. `if` and `else` are new
{term}`keywords <keyword>`. They cannot be used as variable or function names.
Notice also that the statements under the `if` or `else` are indented just like
a function body or the body of a while loop.

How can we use an if-statement to help us simulate tossing a coin? Well, a coin has two sides, heads and tails. We could randomly generate one of two numbers, say 0 and 1, and assign one to be heads and the other to be tails. Thus, we could use `random.randrange(2)`:

```{code-block} python
:linenos:
import random
x = random.randrange(2)

if x == 0:
    print("Heads") 
else:
    print("Tails")
```

On line 5, assigning heads when we choose 0 is, of course, arbitrary. We could
have just as easily made tails be when we choose 0.

It's also possible to use `random.random()`:

```{code-block} python
:linenos:

import random
x = random.random()

if x < 0.5:
    print("Heads") 
else:
    print("Tails")
```

Here, again, the choice to make less than 0.5 be heads is arbitrary. We could have just as easily made it be tails.

Using either `random.random()` or `random.randrange()` is fine for this task.
One way is not particularly better than the other. Using `random.random()`,
however, makes it a little easier to simulate tossing an *unfair* coin. For
example, a coin that comes up heads two-thirds of the time. 

```{code-block} python
:linenos:

import random
x = random.random()

if x < 2/3:
    print("Heads")
else:
    print("Tails")
```

If the random number generator is uniform then this should ensure that `x` is
less than `2/3`, well, with probability `2/3`. This is easier to visualize on a
number line as shown in @fig-probability-interval. If we want to simulate a coin
toss or any other even that happens with a probability $p$, then we can split
the number line from 0 to 1 into two intervals, one from 0 to $p$ and the other
from $p$ to 1. If we pick a random number from 0 to 1, then the probability that
it falls in the first interval is $p$ and the probability that it falls in the
second interval is $1-p$.

```{figure} img/fig-probability-interval.svg
:align: center
:alt: Probability Interval
:label: fig-probability-interval
The interval from 0 to 1 is divided into two subintervals, one from 0 to $p$, where $p$ is the probability of an event, and the other from $p$ to 1. If we pick a random number from 0 to 1, then the probability that it falls in the first interval is $p$ and the probability that it falls in the second interval is $1-p$.
```


:::{exercise}
:label: ex-even-odd

Write a program that reads an integer from the keyboard and prints `even`, if
the number was even, or `odd` if the number was odd. A number is even if it is
divisible by two. That is, the remainder after dividing by two is zero.

:::
:::{solution} ex-even-odd

```{code-block} python
:linenos:

n = int(input("Enter an integer: "))

if n % 2 == 0:
    print(n, "is even")
else:
    print(n, "is odd")
```
:::

### if-elif-else

Let's take an example of tossing a single die.[^die] We will print `one` if we rolled a one, `two` if we rolled a two, etc. One way to write this:

[^die]: Note: *die* is the singular of the plural *dice*, one die, a pair of
    dice

```{code-block} python
:linenos:

import random

# Note that we choose 7 to get a number in the range 1 to 6 inclusive
d = random.randrange(1, 7)
if d == 1:
    print("one")
else:
    if d == 2:
        print("two")
    else:
        if d == 3:
            print("three")
        else:
            if d == 4:
                print("four")
            else:
                if d == 5:
                    print("five")
                else:
                    print("six")
```

This is pretty confusing and not very readable. Most programming languages have an alternative form of the if-statement that we sometimes call *if-else-if*. Here is MicroPython's version:

```{code-block} python
:linenos:
if 〈condition1〉:
    stmts1
elif 〈condition2〉:
    stmts2
elif 〈condition3〉:
    stmts3

...

else:             
    stmts_else
```

The final `else` clause is optional. Note the new keyword `elif`. `〈condition1〉` is checked first and if it is true then `stmts1` is executed, and the remainder of the if-elif-statement is skipped. If `〈condition1〉` is false we check `〈condition2〉` and so on. 

Now we can write our die toss program as:

```{code-block} python
:linenos:

d = random.randrange(6) + 1
if d == 1:                 
    print("one")
elif d == 2:                  
    print("two")
elif d == 3:
    print("three")
elif d == 4:
    print("four")
elif d == 5:
    print("five")
else:
    print("six")
```

## Logical Operators

Up until now our conditions in either the while loop or the if-statement have
been relatively simple. MicroPython, as do all other programming languages,
allow you to state more complicated conditions such as, *if the temperature
greater than 50 and less than 100*. We have new Python keywords `and`, `or`,
`not`.

### Logical `and`

Let's say we rolled a pair of dice and wanted to check if we rolled two ones (snake eyes). Our first attempt, might be:

```{code-block} python
:linenos:

d1 = random.randrange(1, 7)
d2 = random.randrange(1, 7)

if d1 == 1:
    if d2 == 1:
        print("snake eyes!")
```

This works just fine, albeit a bit clunky. More concise would be to use the logical operator `and`.

```{code-block} python
:linenos:

d1 = random.randrange(1, 7)
d2 = random.randrange(1, 7)

if d1 == 1 and d2 == 1:  
    print("snake eyes!")
```

The logical operator `and` combines a logical value on the left and the right,
*X* `and` *Y*. The entire logical expression is `True` if both *X* and *Y* are
`True`, but `False` otherwise. We often state this in terms of a {term}`truth table`. 

The truth table for logical `and` is:

| X | Y | X `and` Y |
|---|---|-----------|
| `False` | `False` | `False` |
| `False` | `True` | `False` |
| `True` | `False` | `False` |
| `True` | `True` | `True` |


:::{exercise}
:label: ex-and-operator

Write an if-statement that checks whether an integer `n` is between 0 and 100
inclusive. If it is then set a variable `x` to `0`. Write it two ways, one using
a nested if-statement, and the second using the logical `and` operator.

:::
:::{solution} ex-and-operator

**Version 1**

```{code-block} python
:linenos:

if n >= 0:
    if n <= 100:
        x = 0
```

**Version 2**

```{code-block} python
:linenos:

if n >= 0 and n <= 100:
    x = 0
```
:::

These are not complete programs as we haven't assigned a value to `n` yet. We
will often call these {term}`code fragments <code fragment>`.

### Logical `or`

Returning to our dice roll, let's check to see if at least one of the dice is a
one. Again, your first instinct might be to write this using if-statements
alone, which is possible.

```{code-block} python
:linenos:

d1 = random.randrange(1, 7)
d2 = random.randrange(1, 7)

if d1 == 1:
    print("one")
elif d2 == 1:
    print("one")
```

But a more concise way would be to use the logical `or` operator.

```{code-block} python
:linenos:

d1 = random.randrange(1, 7)
d2 = random.randrange(1, 7)

if d1 == 1 or d2 == 1: 
    print("one")
```

The logical operator `or` combines a logical value on the left and the right,
*X* `or` *Y*. The entire logical expression is true if either one of *X* or *Y*
is true. The truth table for logical `or` is:

| X | Y | X `or` Y |
|---|---|----------|
| `False` | `False` | `False` |
| `False` | `True` | `True` |
| `True` | `False` | `True` |
| `True` | `True` | `True` |

:::{important}
When `and` and `or` are both used in an expression `and` has a higher precedence
(much like `*` does over `+`).
:::

:::{exercise}
:label: ex-xor-operator

Write a code fragment that will determine whether a user rolled exactly one 1. 
Assume variable `d1` and `d2` have values.

:::
:::{solution} ex-xor-operator
:class: dropdown

There are several ways to write this. Here is one way.

```{code-block} python
:linenos:

if (d1 == 1 or d2 == 1) and d1 != d2:  # (1)
    print("exactly one, 1")
```

(1) The parentheses around the `or` are necessary. 

Another solution is:

```{code-block} python
:linenos:

if (d1 == 1 or d2 == 1) and (d1 != 1 or d2 != 1):  # (1)
    print("exactly one, 1")
```

(1) Note the parentheses, they are necessary.

Yet a third solution is:

```{code-block} python
:linenos:

if (d1 == 1 and d2 != 1) or (d1 != 1 and d2 == 1):
    print("exactly one, 1")
```
:::

### Logical `not`

The remaining logical operator is `not`, the logical negation of `True` and
`False`. The truth table is simply:

| X | `not` X |
|---|---------|
| `False` | `True` |
| `True` | `False` |

## Additional Exercises

:::{exercise}
:label: ex-max2

Write a function `max2` that returns the larger of the two parameters. For
example, `print(max2(9,7))` would print `9`.

:::
:::{solution} ex-max2
:class: dropdown


```{code-block} python

def max2(x,y):
    if x > y:
        return x
    else:
        return y
```

:::

:::{exercise}
:label: ex-max3

Write a function `max3` that returns the maximum of three parameters. For
example, `print(max3(4,2,9))` would print `9`.

:::
:::{solution} ex-max3
:class: dropdown

```{code-block} python
:linenos:

def max3(x,y,z):
    if x > y and x > z:    # (1)
        return x
    elif y > x and y > z:  # (2)
        return y
    else:                  # (3)
        return z
```

(1) Is `x` the largest?
(2) Is `y` the largest?
(3) It must be `z`

A more concise way would be to use the function `max2` from the previous problem.

```{code-block} python
:linenos:

def max3(x,y,z):
    return max2(x,max2(y,z)) 
```
:::


:::{note}

Both exercises above are a bit unnecessary. MicroPython already has a built-in
function `max` that can take an arbitrary number of arguments.

```{code-block} python
:linenos:
print(max(4,1))
print(max(4,1,9))
print(max(2,10,4,1))
```
:::

:::{exercise}
:label: ex-middle

Write a function `middle` that returns middle of three numbers. Calling
`print(middle(4,1,9))` would print `4`.

:::

:::{exercise}
:label: ex-equal-not-equal

Write a program that reads three integers from the user and prints `equal` if
all three are equal and `not equal` if they are not all the same.
:::
:::{solution} ex-equal-not-equal
:class: dropdown

```{code-block} python
:linenos:

x = int(input("Enter number: "))
y = int(input("Enter number: "))
z = int(input("Enter number: "))

if x == y and y == z:
    print('equal')
else:
    print('not equal')
```
:::