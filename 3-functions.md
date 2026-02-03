# Functions 

Functions play a massively important role in programming. They encapsulate
common computations and keep programmers from having to reinvent the wheel. You
can just use the `math.sqrt` function. You don't have to write it yourself. For
complex operations (for example, printing to the console), functions also
*abstract* away much of the hard work. You just call `print("Hello World")` and
the function takes care of all the details of getting the text to appear on the
console.

Recall that in mathematics a {term}`function` maps values in a *domain* to
values in a *range*. In Python the `math.sqrt` function maps 4 to 2.0, 9 to 3.0,
and 2 to 1.4142135623730951 as shown in @fig-sqrt-func.[^irrational]

[^irrational]: This is only an approximation. The $\sqrt{2}$ is *irrational*. That is, it is a never ending, non-repeating sequence of digits.

```{figure} img/sqrt-func.png
:label: fig-sqrt-func
:width: 604px
:align: center

`math.sqrt` function
```

The round function maps `round(3.56,1)` to `3.6`. In MicroPython, ***functions always return a value***. Always. The value returned by a function can be used in a number of ways:

* It can be assigned to a variable.
* It can be passed as an argument to another function.
* It can be combined with other values in an arithmetic expression (e.g., using `*` or `+`).

Sometimes we don't care about the return value. In MicroPython functions
sometimes return the special value `None`, which essentially means the function
does not "really" return a value.[^void] For example, @fig-print-func shows that
the `print` function returns the value `None` but has the *side effect* of
printing its arguments on the console.

`None` is the only value that is part of the `NoneType` data type. That means
that `None` is not an integer, float, string, or any other data type. It is its
own special type. The `NoneType` contains only one value, and does not support
any operations.

[^void]: In other programming languages such as C and Java these are called *void* functions.

```{figure} img/print-func.png
:label: fig-print-func
:width: 604px
:align: center

The `print` function returns `None` regardless of its arguments, but it prints to the console as a side effect.
```

We saw earlier that 

```{code-block} python
:linenos:
print("Hello World")
```

will print *Hello World* on the console, but `print` also returned the `None`
value.

The following looks strange, but is legit, and almost certainly not what was
intended.

```{code-block} python
:linenos:
print(print("Hello World"))
```

:::{exercise} 
:label: ex-print-none

What would get printed by the following code?

```{code-block} python
:linenos:
ret_val = print("Hello World")
print(ret_val)
```

:::
:::{solution} ex-print-none
:class: dropdown

```sh
Hello World
None
```
:::

The assignment statement with `print` prints *Hello World* to the console and
returns `None`, which is store in the variable `ret_val`. The second `print`
statement prints the value of `ret_val` to the console. Again, strange, and
almost certainly not what was intended. :::


## Calling Functions

Lets get a little more formal about calling functions. Consider the statement

```{code-block} python
:linenos:
print("Hello World")
```

We say that we are *calling* the `print` function and *passing* the argument
`Hello World`. Passing an argument means we send the value to the function.

Consider the following program:

```{code-block} python
:linenos:
import math
result = math.sin(math.sqrt(math.pi/4))
print(round(result, 2))
```

:::{exercise}
:label: ex-func-calls

How many function calls are there in the three lines above? Explain all of the arguments and return values.
:::
:::{solution} ex-func-calls
:class: dropdown

The first line contains two function calls. First `math.sqrt` is called with the
argument `math.pi/4`. Then `math.sin` is called and uses the value returned from
the `math.sqrt` call as its arguments. The return value of `math.sin` is then
assigned to the variable `result`. The second line contains two function calls
as well. First `round` is called with _two_ arguments, `result` and `2`.
`result` is the value being rounded and `2` is the number of places to round to.
The return value from `round` is then used as the only argument to the `print`
function. 

In total there are four function calls and five arguments involved.
:::

## Defining Functions

The real power with functions is that programmers get to define our own.
Functions allow us to encapsulate commonly occurring computations. Let's go back
to our rather banal example of our formula to convert a Fahrenheit temperature
to Celsius. Rather than having to keep remembering the formula we can just
define a function.

```{code-block} python
:linenos:

def f2c(f):              # (1)
    c = 5 / 9 * (f - 32) # (2)
    return c             # (3)
```

Let's break down what is going on in the code.

1. This is the *function header*. It tells Python we are defining our own
   function and it takes one {term}`parameter` `f`. The value of `f` is
   determined by the argument when `f2c` is called.
2. This is the main part of the function that does the computation. It defines a
   {term}`local variable` `c`.
3. This is the return statement that indicates that function `f2c` returns the
   value `c` to the *caller* that was just computed.

Lines 2 and 3 constitute the *function body*, which is indented under the
function header.

We now have our own function for converting Fahrenheit to Celsius, and we can
save it in a file somewhere, so we can reuse it later.

We can use `f2c` in a program by *calling* it with an argument.

```{code-block} python
:linenos:
print(f2c(32))
```

We call this the *main program*. The main program is any code that exists
outside of a function.

:::{exercise}
:label: ex-f2c-call-incorrect

Why is the following line incorrect?  
`f2c(32)`
:::
:::{solution} ex-f2c-call-incorrect
:class: dropdown

Because `f2c` returns a value, and this line does not do anything with that
value, it is a wasted call to `f2c`. It doesn't print it or use it in
another computation. 
:::

It is a common mistake for students to confuse a function *returning a value*
and a *function printing a value*. Consider this version of `f2c`.

```{code-block} python
:linenos:
def f2c(f):
    c = 5 / 9 * (f - 32)
    print(c)
```

This function returns the value `None` and, as a side effect, prints the value
of the variable `c` on the console. This function is not technically wrong. It
does not have a syntax error, nor a run-time error, or even a logic error. But
it is in some way inferior to the first version of `f2c`. Consider the following
program.

```{code-block} python
:linenos:
t = float(input("Enter a temperature: "))
print(f2c(t) +  100)
```

This program reads a temperature from the user and puts it in the variable `t`.
It then converts `t` to Celsius and adds 100 degrees Celsius to the result and
printing the final value. For the first version of `f2c` this works fine. But
the second version crashes because it tries to add 100 to `None`.
 
:::{warning}
A function that returns a value is not the same thing as the function printing a
value.
:::

### Putting functions in a module

Since we will be using the `f2c` function later in the text it is a good idea to place general functions in a module, such as `util.py`.

```{code-block} python
:linenos:
import util

t = float(input("Enter a temperature: "))
print(util.f2c(t) +  100)
```

## Functions for their side effect

Functions return values. Some functions, such as `print`, return `None` but are used for their *side effect*.  
 
Recall our circuit from before where we connected an LED to the microcontroller.

```{figure} img/fig-led-circuit.png
:label: fig-led-circuit-again
:align: center

An LED connected to a microcontroller pin with a current limiting resistor.
```

What if we wanted to blink the LED multiple times? What if we wanted to blink
two different LEDs? One possibility is to copy and paste the code to turn the LED
on and off multiple times. But that would be tedious and error-prone. A better
way is to define a function that turns the LED on and off. The function does not
return a value, but it has the side effect of blinking the LED. 

We will need a function that takes as parameters a pin object and the number of milliseconds to keep the LED on:

```{code-block} python
:linenos:
def blink(pin, duration_ms):
    '''
    Turn on the LED connected to pin for duration_ms milliseconds,
    then turn it off.
    :param: pin: a machine.Pin object configured for output
    :param: duration_ms: number of milliseconds to keep the LED on
    '''
    pass
```

This is just the function header. The MicroPython statement `pass` is the
statement that does nothing. We are using it here as a placeholder for the
function body, which we have not yet written.

So what we'll do now is place all of the code used for the blinking inside the function and make sure that we use the parameters.

```{code-block} python
:linenos:
import time

def blink(pin, duration_ms):
    '''
    Turn on the LED connected to pin for duration_ms milliseconds,
    then turn it off.
    :param: pin: a machine.Pin object configured for output
    :param: duration_ms: number of milliseconds to keep the LED on
    '''
    
    # turn on the LED
    pin.on()

    # wait duration_ms milliseconds
    time.sleep_ms(duration_ms)

    # turn off the LED
    pin.off()
```

Now we can call the `blink` function as many times as we like without having to 
duplicate lots of code. The variables `pin` and `duration_ms` are *parameters* and they can be used anywhere in the function body. That is their {term}`scope`.

All of the other variables that are defined in the function are *local variables*. A local variable's scope is from the point where where it is defined until the end of the function.

```{note}
A *local variable* is defined in a function. Its scope is the point from where it was defined until the end of the function.
```

### Example: Blinking an LED

```{code-block} python
:linenos:
import machine
import time

led = machine.Pin(32, machine.Pin.OUT)

# blink the LED for 500 ms
blink(led, 500)

time.sleep(1)

# blink the LED for 200 ms
blink(led, 200)

```


## Benefits of functions

### Functions make code more readable 

If you look at the main program above it is clear that the program draws four
figures. If we didn't use a function and duplicated the code to draw the figures
then it would be far less clear what is going on. 

### Functions make code less buggy

Imagine had we not used a function and we found an error in the code, we would
then have to fix that error in every place where the code was duplicated. When
we use a function we just fix it once.

### Functions make programs more concise

This one is obvious. We don't have to copy and paste code, and the program is
much shorter.

### Functions allow programmers to easily *reuse* code.

Consider our Fahrenheit-to-Celsius conversion function `f2c` that we placed in a
file `util.py`. We can reuse that function whenever we want without having to
reinvent the wheel every time.

## Additional Exercises

:::{exercise}
Write a function `circ_area` that that takes the radius of a circle as a
parameter and returns the area of the circle. Write a main program that reads
the radius from the user (keyboard) and prints the area.
:::

:::{exercise}
Answer questions about the program below.

```{code-block} python
:linenos:
x = 5                   
y = 6                   
z = 33                  

def f(x):               
   y = 9                
   print(x + y + z)     

print(x + y + z)        
f(12)                   
print(x + y + z)        
pass
```

1. What is the output of the program?
2. Which line contains a function header?
3. Which line(s) constitute the main program?
4. Is there a local variable defined anywhere? If so what is its scope?
5. Does the function `f` return a value?
6. Does the function `f` reference any global variables?
7. Which lines constitute a function body?
8. Are there any arguments used in the program? If so what and where are they? (tricky)
9. Are there any parameters defined in the program? Explain.
10. What does the last line do?
:::

:::{exercise}
What is a *built-in* function?
:::

:::{exercise}
:label: ex-investment

Assume that **_C_** is an initial amount of an investment, **_r_** is the yearly rate of interest (e.g., .02 is 2%), **_t_** is the number of years until maturation, **_n_** is the number of times the interest is compounded per year, then the final value of the investment is $p=c(1+r/n)^{tn}$. Write a function `investment` that takes **_C_**, **_r_**, **_n_**, and **_t_** as arguments and returns the final value of the investment to the nearest penny. Test your function with a main program where $C = 1000, r = .01, n = 1, t = 1$.
:::
:::{solution} ex-investment
:class: dropdown

```{code-block} python
:linenos:
def investment(c,r,n,t):
    p = c*(1 + r/n)**(t*n)
    return p 
```

Note that we didn't have to use the local variable `p`. We could just as well
have said `return c*(1 + r/n)**(t*n)`

Test on $C = 1000, r = .01, n = 1, t = 1$.

```python
print(investment(1000,.01,1,1)) 
```
This should print `1010.0`
```
:::

:::{exercise}

Write a function `dot` and a function `dash` that generate morse code blinks. 
Use a blink of 0.2 seconds for a dot, 0.6 seconds for a dash. In both cases, 
pause for 0.2 seconds after.

Test your program by outputting the international distress signal SOS (`...---...`).

HINT: Call the `blink` function defined earlier.

:::


