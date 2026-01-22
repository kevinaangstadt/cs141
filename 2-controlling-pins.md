# Controlling Pins with MicroPython

## Libraries and Modules
There is a lot of code already written in MicroPython that we can use in our own
programs. This code is distributed as a {term}`library` that contains functions
and variables that we can use to perform common tasks. Much like a library we
might go to for books, we have to explicitly go to the library and "check out"
the code before we are able to use it in our programs.

MicroPython comes with a library of code built-in as standard, and thus we call
this the *standard library*. However, other developers can provide additional
libraries. We often call these *third-party libraries*.

### Math Module

One collection of code in the standard library is called the `math`
{term}`module`. A module is a collection of related functions and variables that
are grouped together in a file. Modules can be hierarchical, that is we can have
modules defined inside other modules. Much like on your computer where you can
have folders inside folders to organize your documents.

The math module contains many math related functions and some predefined
constants. For example `math.sin(x)` computes the $\sin$ of the argument `x`
(where `x` is in radians).

To use the functions and definitions in the math module your program first needs
to tell MicroPython that we need it using an *import statement*.

```{code-block} python
:linenos:
import math
```

One way to compute the square root of a number would be just to raise to the 1/2 power. 

```{code-block} python
:linenos:
print(2**.5)
```

Another way would be to use the math module's square root function.

```{code-block} python
:linenos:
print(math.sqrt(2))
```

:::{tip}
`import` is a MicroPython *keyword*. A keyword is a word reserved for use by MicroPython. 
As such you should never use a keyword as a variable name (in fact that is an error). 
:::

A constant defined in the math module is `math.pi`

```{code-block} python
:linenos:
print(math.pi)
```

```{code-block} console
3.141592653589793
```

:::{note} 
To reference functions and definitions in a module use *dot notation*. For example, `math.pi` or `math.sqrt(x)`.
:::

### Time Module
Another useful module is the `time` module. This module contains functions for
working with time-related tasks. One function in this module is `sleep(seconds)`
which pauses the execution of the program for the specified number of seconds.

```{code-block} python
:linenos:
import time

print("Hello")
time.sleep(2)  # Pause for 2 seconds
print("World")
```

This program will print "Hello", wait for 2 seconds, and then print "World".

## Controlling a Pin on the Microcontroller

The physical pins on a microcontroller allow us to interface with external
components such as input sensors or output displays and actuators. We will start
by using a pin to output a digital signal (i.e., turn it on or off).

When a pin is turned *on*, it outputs a voltage (typically 3.3V or 5V depending
on the microcontroller). This means that electrical current can flow from the
pin, through other components, and back to ground.

When a pin is turned *off*, it is connected to ground (0V). This means that no
current can flow from the pin.

### Turning an LED On and Off
Our first example of an output pin will be to turn a light-emitting diode (LED)
on and off. An LED is a special component that emits light when electrical
current flows through it. LEDs are polarized components, meaning they have a
positive (anode) and negative (cathode) lead. A {term}`diode` only allows
current to flow from the anode to the cathode. If we connected a higher voltage
to the cathode, no current would flow and the LED would not light up.

LEDs can only handle a limited amount of electrical current before they are
damaged and no longer work. Our microcontroller pins can supply more current
than an LED can handle, so we need to use an additional device called a
{term}`resistor` to absorb the addition current. In this sense, it *limits* the
current flowing through the LED to a safe level, so we refer to this use of a
resistor as a *current-limiting resistor*.

:::{hint}
The long leg of the LED is the anode (positive) and should be connected to the
microcontroller pin. The short leg is the cathode (negative) and should be
connected to ground (0V).
:::

How do we pick the correct value for the current-limiting resistor? We need to
know a few bits of information:
- The *forward voltage* or voltage needed to turn on the LED
- The maximum current the LED can handle safely
- The voltage output by the microcontroller pin when it is turned on

With this information, we can use Ohm's Law to calculate the appropriate resistance value for the current-limiting resistor.

$$ V = I \cdot R $$

Where:
- $V$ is the voltage across the resistor
- $I$ is the current through the resistor
- $R$ is the resistance

We can rearrange this formula to solve for $R$:

$$ R = \frac{V}{I} $$

To find the voltage across the resistor, we subtract the forward voltage of the
LED from the voltage output by the microcontroller pin. We then divide this by
the current we want to allow through the LED to find the resistance.

:::{exercise}
:label: ex-led-resistor

Given an LED with a forward voltage of 2.0V and a maximum current of 6mA
(0.006A), and a microcontroller pin that outputs 3.3V when turned on, calculate
the value of the current-limiting resistor needed to safely operate the LED.

:::
:::{solution} ex-led-resistor
First, we need to find the voltage across the resistor. This is the difference
between the voltage output by the microcontroller pin and the forward voltage of
the LED: $$ V_{resistor} = V_{pin} - V_{LED} = 3.3V - 2.0V = 1.3V $$

Next, we can use Ohm's Law to calculate the resistance:
$$ R = \frac{V_{resistor}}{I} = \frac{1.3V}{0.006A} = 216.67\Omega $$

We would typically round this up to the nearest standard resistor value, which is
220Ω.
:::

## Wiring up the Circuit
We will make use of a *breadboard* to build our circuit. Breadboards are used to
prototype circuits without soldering. They have a series of holes that are
connected together in a specific pattern. The holes are used to insert wires and
components to build a circuit.

There are two main types of connected holes on a breadboard: *power rails* and
*terminal strips*. Power rails are used to distribute power to the circuit, while
terminal strips are used to connect components together. Power rails run the
entire length of the breadboard (all holes in a row are connected), while
terminal strips are connected in groups of five. There is a gap between the rows
of terminal strips to allow for DIPs to be inserted.

Items you will need:
- ESP32 board
- Red LED (note that the longer leg is the anode (+))
- 200Ω resistor
- Breadboard
- Jumper wires (x2)

Wire up the circuit as shown in @fig-led-circuit.

```{figure} ./img/fig-led-circuit.png
:label: fig-led-circuit
:alt: Circuit diagram showing an LED connected to a microcontroller pin through a current-limiting resistor
:align: center  

Circuit diagram showing an LED connected to a microcontroller pin through a current-limiting resistor

```
Note that one wire is connected to GPIO pin 32 and the other is connect to ground (GND).

## Writing the MicroPython Code to Control the LED
MicroPython includes a special module called `machine` that provides functions
and operations for controlling hardware components of the microcontroller. 

One operation provided by the `machine` module is a function to access a specific pin:

```{code-block} python
:linenos:
import machine
import time

led = machine.Pin(32, machine.Pin.OUT)
```

The `Pin` function takes two arguments: the pin number (in this case 32) and the mode
(which can be either `machine.Pin.IN` for input or `machine.Pin.OUT` for output).
Since we want to control the LED, we set the mode to output.

Most of the variables we have encountered so far have held strings, integers, or
floats. The variable `led` above represents a *reference* to an Pin object. For
now, think of a reference as being a variable that refers to a complex object
such as a pin or display.

:::{note} 
An *object* in MicroPython is a value (not unlike an integer or a float) that 
contains functions for accessing the data in the object. Functions associated 
with objects are called *methods*.
:::

For example, a Pin object has a method `on()` that turns the pin on and a method
`off()` that turns the pin off. Methods are always called using a *dot notation*
of the object name followed by the methods. For example, `led.on()`.

We can use the `time` module's `sleep()` function to create a delay between
turning the LED on and off. Here is the rest of our program to blink the LED:

```{code-block} python
:linenos:
:lineno-start: 5
led.on()  # Turn the LED on
time.sleep(1)  # Wait for 1 second
led.off()  # Turn the LED off
```

:::{exercise}
:label: ex-blink-led-pause
Can you think of a way to keep the LED on until the user presses return on the keyboard?
:::
:::{solution} ex-blink-led-pause
:class: dropdown
You can use the `input()` built-in function to wait for user input before turning off the LED:

```{code-block} python
:linenos:
import machine

led = machine.Pin(32, machine.Pin.OUT)
led.on()  # Turn the LED on
input("Press Enter to turn off the LED...")  # Wait for user input
led.off()  # Turn the LED off
```
:::
