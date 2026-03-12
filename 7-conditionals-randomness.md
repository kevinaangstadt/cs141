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

## Counting Rolls

How hard is it to roll snake eyes? Well, we have a 1 in 6 chance of rolling a
one on the first die and a 1 in 6 chance of rolling a one on the second die.
Because these are *independent* events, we can multiply the probabilities
together to calculate a probability of 1 in 36 of rolling snake eyes. We can
verify this by simulating rolling a pair of dice many times and counting how
many times we rolled snake eyes.

Let's print out our answer to the LCD when we have an answer. As shown in
@fig-lcd, the LCD connects to the I2C bus using GPIO pins 21 and 22. The LCD
requires 5V to power the backlight.

```{figure} img/fig-lcd-only.png
:align: center
:alt: LCD
:label: fig-lcd
A 16x2 LCD connected to the I2C bus using GPIO pins 21 and 22.
``` 

```{code-block} python
:linenos:
# simulate rolling two dice until we get both 1s

import machine
import random

import lcd_i2c

# create an I2C object to access the I2C serial communication bus
i2c = machine.I2C(1, sda=machine.Pin(21), scl=machine.Pin(22))

# make an LCD object to control the 16x2 display
lcd = lcd_i2c.LCD(0x27, 16, 2, i2c=i2c)
lcd.begin()

# are we done rolling?
done = False
count = 0

# keep rolling until we get snake eyes
# we use a `done` variable to keep track of whether we are done or not,
# which makes for a simple looping structure where we only have to set
# `done` to `True` when we get snake eyes
while not done:

    # roll two dice
    roll1 = random.randrange(1, 7)
    roll2 = random.randrange(1, 7)
    count += 1

    if roll1 == 1 and roll2 == 1:
        # mark that we are done
        done = True
        lcd.print("Snake Eyes")

# print the total count
# move to second line
lcd.set_cursor(0,1)
lcd.print(f"{count} rolls")
```

What happens when you run this code? We should see `Snake Eyes` on the first
line of the LCD and the number of rolls it took to get snake eyes on the second
line. If we run this code multiple times, we should see that it takes about 36
rolls on average to get snake eyes. Sometimes, you will get very lucky and get
snake eyes on the first roll, and sometimes you will get very unlucky and have
to roll hundreds of times before you get snake eyes.

## Triggering Conditional Events
In the previous chapter, we measured the temperature using a thermistor. What if
we wanted to trigger an event when the temperature exceeds a certain threshold?
For example, we could turn on a fan or illuminate a warning light when the
temperature exceeds some threshold.

### Wiring Up the Circuit
We will extend the circuit from the previous chapter to add both an LED and a
button. We will illuminate the LED when the temperature exceeds our threshold
and we will use the button to test that the LED is working. That is, the LED
should light when *either* we press the button or the temperature exceeds our
threshold.

Additional items you will need:
* Pushbutton switch
* Red LED
* 10KΩ resistor
* 220Ω resistor
* Jumper wires

Add the additional components to the circuit as shown in
@fig-lcd-thermistor-led-button. The button is connected to GPIO pin 36 with a
10KΩ pull-down resistor. The LED is connected to GPIO pin 12 with a 220Ω current
limiting resistor.

```{figure} img/fig-lcd-thermistor-led-button.png
:align: center
:alt: LCD, Thermistor, LED, Button Circuit
:label: fig-lcd-thermistor-led-button
A circuit with a 16x2 LCD, a thermistor, an LED, and a button. The LCD is
connected to the I2C bus using GPIO pins 21 and 22. The thermistor is connected 
to GPIO pin 14. The LED is connected to GPIO pin 12. The button is connected to 
GPIO pin 36. This image was created using [Fritzing](http://fritzing.org/).
```

### Modifying the Code
Now we need to modify our code to read the button and turn on the LED when the
button is pressed or when the temperature exceeds our threshold. We will use the
logical `or` operator to check if either condition is true.

The updated lines are highlighted below.

```{code-block} python
:linenos:
:emphasize-lines: 30-34, 46-50
import machine
import math
import time

def read_temperature(thermistor, B, R0, T0):
    """
    Read the temperature from the thermistor in degrees Celsius.
    :param thermistor: an ADC object connected to the thermistor voltage divider
    :param B: the B-Parameter value of the thermistor
    :param R0: the resistance of the thermistor at the reference temperature T0
    :param T0: the reference temperature in Kelvin (typically 298.15 K for 25 degrees Celsius)
    :return: the temperature in degrees Celsius
    """
    # read the ADC value in microvolts and convert it to volts
    V_thermistor = thermistor.read_uv() / 1000000
    
    # convert voltage to resistance using the voltage divider formula
    R_thermistor = 10000 * V_thermistor / (3.3 - V_thermistor)
    
    # calculate temperature using the Steinhart-Hart equation
    T = B * T0 / (T0 * math.log(R_thermistor / R0) + B)
    
    # convert Kelvin to Celsius
    return T - 273.15

# set up the ADC on pin 14
thermistor = machine.ADC(machine.Pin(14, machine.Pin.IN))
thermistor.atten(thermistor.ATTN_11DB)

# create a Pin object for the button on pin 36 with a pull-down resistor
button = machine.Pin(36, machine.Pin.IN)

# create a Pin object for the LED on pin 12
led = machine.Pin(12, machine.Pin.OUT)

# constants for the thermistor
B = 3950    # A typical B-Parameter value for an NTC thermistor
R0 = 10000  # 10K ohms at 25 degrees Celsius
T0 = 298.15 # 25 degrees Celsius in Kelvin

# loop forever and print the temperature every second
while True:
    # call our function to read the temperature
    temperature = read_temperature(thermistor, B, R0, T0)

    # check if the button is pressed or the temperature exceeds 25 degrees
    if button.value() == 1 or temperature > 25:
        led.on()    # turn on the LED
    else:
        led.off()   # turn off the LED

    # Print the temperature rounded to 2 decimal places
    print(f"Temperature: {round(temperature, 2)} C")
    # wait for 1 second before reading again
    time.sleep(1)
```

## Controlling a Fan
Rather than just illuminating an LED, we may want to turn on a fan when the
temperature exceeds a certain threshold. This is common in many devices to help
with cooling. There are many different types of electric motors, but perhaps the
most common type is the *DC motor*. A DC motor has two wires, a positive and a
negative. When you apply a voltage across the wires, the motor spins. The
direction of the spin depends on the polarity of the voltage. If you reverse the
voltage, the motor will spin in the opposite direction.

DC motors typically require more current than a microcontroller can provide, so
we need to use an additional chip called a *motor driver* to control the motor.
The motor driver acts as a switch that can turn the motor on and off, and can
also reverse the voltage to change the direction of the motor. One common motor
driver is the L293D, which can control two DC motors.

A diagram showing the pins of the L293D motor driver is shown in @fig-l293d. The
L293D has two channels, each of which can control a DC motor. Each channel has
two input pins (IN1 and IN2 for channel 1, IN3 and IN4 for channel 2) that
control the direction of the motor, and an enable pin (EN1 for channel 1, EN2
for channel 2) that turns the motor on and off. All of the ground pins are
connected together and should be connected to the ground of the microcontroller.
The power pins are separate. VCC1 is the input voltage to power the IC. VCC2 is
the input voltage to power the motors. The L293D can handle a wide range of
voltages, but for our purposes we will use 5V to power the motors.

The enable pins are "active high", meaning that a high voltage enables the
output (compare this with the 74HC595 shift register, which had an active low
enable pin!). When the channel is enabled, a high input value will result in a
high output value. Thus, we can wire a DC motor across OUT1 and OUT2. If we set
IN1 high and IN2 low, the motor will spin in one direction. If we reverse this,
the motor will spin in reverse.

```{figure} img/L293D_pinout.svg
:align: center
:alt: L293D Motor Driver Pinout
:label: fig-l293d
Pinout of the L293D motor driver. The L293D has two channels, each of which can control a DC motor. Each channel has two input pins (IN1 and IN2 for channel 1, IN3 and IN4 for channel 2) that control the direction of the motor, and an enable pin (EN1 for channel 1, EN2 for channel 2) that turns the motor on and off.
```

### Wiring up the motor.
To control a fan using the L293D, we will connect the fan to one of the channels of the L293D. We will connect the enable pin to 5V so that the output is always enabled. We will connect the input pins to GPIO pins on the microcontroller so that we can control the direction of the motor. The ground of the L293D should be connected to the ground of the microcontroller, and the power pins should be connected to 5V.

We will also connect a {term}`capacitor` across the motor wires to help reduce
electrical noise generated by the motor. A 100nF ceramic capacitor is a good
choice for this (marked with 104). Because the motor spins using magnetic
forces, this can cause fluctuations in the voltage (ripple or spikes) that can
interfere with other electrical signals. A capacitor helps to smooth these out.

Components you will need:
* Breadboard
* L293D motor driver
* DC fan (5V)
* 100nF ceramic capacitor (marked with 104)
* Jumper wires

Wire up the components as shown in @fig-l293d-fan. The fan is connected to OUT1 and OUT2 of the L293D. The enable pin EN1 is connected to 5V. The input pins IN1 and IN2 are connected to GPIO pins 32 and 33, respectively.

```{figure} img/fig-h-bridge-motor.png
:align: center
:alt: L293D Motor Driver with Fan
:label: fig-l293d-fan
A circuit with an L293D motor driver controlling a DC fan. The fan is connected to OUT1 and OUT2 of the L293D. The enable pin EN1 is connected to 5V. The input pins IN1 and IN2 are connected to GPIO pins 32 and 33, respectively. A 100nF ceramic capacitor is connected across the motor wires to help reduce electrical noise generated by the motor.
```

### Writing the Code
Let's write some code to control the fan. We will show this in isolation first, to give you a clean example.

```{code-block} python
:linenos:
import machine
import time

# create Pin objects for the motor control pins
motor1 = machine.Pin(32, machine.Pin.OUT)
motor2 = machine.Pin(33, machine.Pin.OUT)

# loop forever
while True:
    # turn on the motor in one direction
    motor1.on()   # IN1 high
    motor2.off()  # IN2 low
    time.sleep(1)

    # turn on the motor in the other direction
    motor1.off()  # IN1 low
    motor2.on()   # IN2 high
    time.sleep(1)
```
This code will turn the motor on in one direction for 1 second, then reverse the
direction for 1 second, and repeat this indefinitely. You should see the fan
spin in one direction, then reverse and spin in the other direction. One
direction should push air, while the other direction pulls air.

:::{warning}

The fan uses a lot of current, so the USB connection to the ESP32 is likely
insufficient to power everything. You may need to wire in a separate 5V power
supply to power the fan and the L293D. Make sure to connect the ground of the
separate power supply to the ground of the ESP32. If your ESP32 kit has a
lithium battery connector, you can use this.

:::

:::{note}

Even with the capacitor to reduce electrical noise, you may still see some strange behavior. Some USB connections are more finicky than others (e.g., the authors had trouble connecting the ESP32 directly to an Apple MacBook Air while running the fan) and might disconnect when the fan turns on.

Two possible solutions to this are to use a powered USB hub between the ESP32 or
reduce the input voltage to the L293D to 3.3V. This will make the fan spin more
slowly, but it also reduces the current draw and ripple.

:::

### Varying the Speed of the Fan
As with many other components, we can vary the speed of the fan by using a
technique called *pulse width modulation* (PWM). Recall that this technique
turns a pin on and off repeatedly to produce a "dimming" effect. With a motor controller, it is important to use a very high frequency for the PWM signal, such as 20KHz, otherwise you may hear a high-pitched whine coming from the motor. The L293D can handle PWM signals on the input pins, so we can use the `PWM` class from the `machine` module to generate a PWM signal on the input pins.

```{code-block} python
:linenos:
import machine
import time

# create PWM objects for the motor control pins
motor1 = machine.PWM(machine.Pin(32))  # IN1
motor2 = machine.PWM(machine.Pin(33))  # IN2

# set frequency to 20KHz
motor1.freq(20000)  
motor2.freq(20000)

# slowly turn the fan on
duty = 0
while duty <= 1023:
    motor1.duty(duty)  # IN1 duty cycle
    motor2.duty(0)     # IN2 off
    duty += 10
    time.sleep_ms(100)
```

:::{exercise}
:label: ex-fan-control
Modify the code from the previous section to turn on the fan when the button is
pressed or when the temperature exceeds 25 degrees Celsius. The fan should turn off when the button is not pressed and the temperature is below 25 degrees Celsius.
:::


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