# Parallel and Serial Data

## Controlling Multiple Pins

So far, we have only controlled one pin and one LED on our microcontroller. There is nothing stopping us from controlling multiple pins at the same time. 
An important consideration is which pins are available on our microcontroller. Each microcontroller has a different number of pins and different capabilities for each pin. For example, some pins may support analog input while others only support digital input/output.

We have been using the ESP32 microcontroller on the standard development board. Referencing @fig-esp32-pins, we can see that there are many pins available for general-purpose input/output (GPIO). For example, GPIO34-36 and GPIO39 are input-only pins. On the ESP32, most pins are able to be used for PWM output. Several pins are also restricted (e.g., GPIO 6-11). 

```{figure} ./img/esp32_devkitC_v4_pinlayout.png
:label: fig-esp32-pins
:alt: Pin layout diagram for the ESP32 DevKitC v4 development board
:align: center

Pin layout diagram for the ESP32 DevKitC v4 development board. Image from [Espressif](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html).
```

## Seven Segment LED Display
A common electronic component that uses multiple pins is a seven-segment LED display. This display consists of seven individual LEDs arranged in a figure-eight pattern, along with an optional eighth LED for the decimal point. By controlling which segments are lit, we can display numbers and some letters.

```{figure} ./img/7segment_pinout.svg
:label: fig-7segment
:alt: Pinout diagram for a common cathode seven-segment LED display
:align: center
Pinout diagram for a common cathode seven-segment LED display. Segments and pins are labeled.
```

This particular seven-segment display is a *common cathode* type, meaning that all the cathodes (negative terminals) of the LEDs are connected together internally. There are two pins on the LED that connect to this common cathode, and we will need to connect at least one of these to ground.

To light up a segment, we need to connect the corresponding pin to a positive voltage (e.g., 3.3V or 5V) through a current-limiting resistor.

:::{caution}
It might be tempting to connect the common cathode to ground using a single current limiting resistor. After all, all of the LED segments will flow through this one path. However, there is a major drawback to this approach. The LED will become dimmer as more segments are lit because the current is shared among all the segments.

We can use Ohm's law to see why this is the case. Suppose we want to light up three segments, each requiring 2mA of current at 3.3V. Let's also assume a standard 220Ω resistor. Ohm's law states that $V = I \cdot R$. That means that the voltage drop across the resistor is: $V_R = I \cdot R = (3 \times 0.002A) \cdot 220\Omega = 1.32V$. This leaves $3.3V - 1.32V = 1.98V$ for the LEDs. If we only light up one segment, the voltage drop across the resistor is $V_R = (1 \times 0.002A) \cdot 220\Omega = 0.44V$, leaving $3.3V - 0.44V = 2.86V$ for the LED. The LED will be much brighter in this case.

Therefore, we should use a separate current-limiting resistor for each segment to ensure consistent brightness.
:::

### Wiring the Seven-Segment Display
To connect the seven-segment display to our microcontroller, we will need to wire each segment pin to a separate GPIO pin on the microcontroller through a current-limiting resistor. 

Items you will need:

- ESP32 board
- Seven-segment LED display (common cathode)
- Eight (8) 220Ω resistors
- Large breadboard
- Jumper wires

Wire up the circuit as shown in @fig-7segment-parallel-circuit. Each segment (a-g) is connected to a separate GPIO pin through a 220 Ohm resistor. The common cathode is connected to ground.

```{figure} ./img/fig-7segment-parallel-circuit.png
:label: fig-7segment-parallel-circuit
:alt: Circuit diagram showing how to connect a seven-segment display to an ESP32 microcontroller using parallel connections
:align: center
Circuit diagram showing how to connect a seven-segment display to an ESP32 microcontroller. Each segment (a-g) is connected to a separate GPIO pin through a 220 Ohm resistor. The common cathode is connected to ground. Figure made with [Fritzing](https://fritzing.org/).
```

### Controlling the Seven-Segment Display
Based on the wiring diagram, we can define which GPIO pins correspond to each segment of the display:

```{table} GPIO Pin Assignments for Seven-Segment Display
:label: tab-7segment-pins
:align: center

| Segment | GPIO Pin |
|:-------:|:--------:|
| A       | GPIO 33  |
| B       | GPIO 32  |
| C       | GPIO 18  |
| D       | GPIO 5   |
| E       | GPIO 17  |
| F       | GPIO 25  |
| G       | GPIO 26  |
| DP      | GPIO 19  |
```

Thus, we can create a list of the GPIO pins in our MicroPython code:

```{code-block} python
:linenos:
import machine

# Each segment is connected to a different GPIO pin
led_a = machine.Pin(33, machine.Pin.OUT)
led_b = machine.Pin(32, machine.Pin.OUT)
led_c = machine.Pin(18, machine.Pin.OUT)
led_d = machine.Pin(5, machine.Pin.OUT)
led_e = machine.Pin(17, machine.Pin.OUT)
led_f = machine.Pin(25, machine.Pin.OUT)
led_g = machine.Pin(26, machine.Pin.OUT)
led_dp = machine.Pin(19, machine.Pin.OUT)

```

Now we can control each segment individually by setting the corresponding pin high or low. For example, to display the number "8", we need to light up all segments except the decimal point:

```{code-block} python
:linenos:
# Light up segments to display "8"
led_a.on()
led_b.on()
led_c.on()
led_d.on()
led_e.on()
led_f.on()
led_g.on()
led_dp.off()  # Decimal point off
```

This is going to get cumbersome quite quickly. One way to make this easier is to define functions for each of the digits we want to display. For example, we can define a function to display the digit "0":

```{code-block} python
:linenos:
# a function to display the digit "0"
# so that we don't have to repeat this code
def display_0():
    '''
    Display the digit "0" on the seven-segment display.
    '''
    led_a.on()
    led_b.on()
    led_c.on()
    led_d.on()
    led_e.on()
    led_f.on()
    led_g.off()
    led_dp.off()

# call this function to display a 0
display_0()

```

The `display_0` function still uses the variables `led_a` through `led_dp`,
which are neither passed as a parameter nor is it defined with the function. The
function assumes `led_a` through `led_dp` are defined in the main program. We
say that these are {term}`global variables <global variable>`, which are variables defined outside of functions and accessible throughout the program.

:::{exercise}
Write functions `display_1` through `display_9` to display the digits 1
through 9 on the seven-segment display.
:::

:::{exercise}
:label: ex-seven-segment-countdown

Using the functions you defined in the previous exercise, write a program
that counts down from 9 to 0, pausing for one second between each digit.
:::
:::{solution} ex-seven-segment-countdown
```{code-block} python
:linenos:
import machine
import time

# Assume led_a through led_dp are defined as before
# Assume display_0 through display_9 functions are defined as before

display_9()
time.sleep(1)
display_8()
time.sleep(1)
display_7()
time.sleep(1)
display_6()
time.sleep(1)
display_5()
time.sleep(1)
display_4()
time.sleep(1)
display_3()
time.sleep(1)
display_2()
time.sleep(1)
display_1()
time.sleep(1)
display_0()
```
:::

## Parallel Data

In the previous example, we used a separate GPIO pin for each segment of the
seven-segment display. To display a digit, we had to set each pin high or low
and then keep all the pins at these levels to show the correct digit. This is an
example of a {term}`parallel data` system, where multiple pieces of information
are transmitted simultaneously across multiple channels (in this case, the GPIO
pins).

Each GPIO pin is used to transmit an "on" or "off" signal for a specific segment
of the display. Since there are only two possible states for each pin, we can
say that this pin outputs a {term}`binary` value (or a base-2 value). We call
this piece of a data a *binary digit* or {term}`bit` for short.

With parallel data, we can transmit multiple bits at the same time over a
collection of wires or a {term}`bus`. In our case, we have a bus of 8 wires (the
GPIO pins) that can transmit 8 bits of data simultaneously. This allows us to
control all the segments of the display at once, which is why we can show a
digit by setting all the pins to the correct levels. In computer science, a
collection of 8 bits is called a {term}`byte`. Therefore, we can say that our
seven-segment display is controlled by a byte of parallel data.

The drawback of parallel data is that it requires a large number of wires (or pins) to transmit multiple bits. For our ESP32 microcontroller, we have about 20 pins available for GPIO, so we can only control a few devices using parallel data before we run out of pins.  A digital clock, for example, would require at least 4 seven-segment displays (for hours and minutes), which would require 32 GPIO pins just for the displays alone. That's more than the number of GPIO pins available on our microcontroller! We will need a different method to control multiple devices without using so many pins.

## Serial Data
As an alternative to using multiple pins to transmit parallel data, we can use a single pin to transmit data one bit at a time. This is called {term}`serial data`. This is a common trade-off in computer science: we can either use more hardware (parallel data) or more time (serial data) to transmit the same information. Often, this trade-off depends on the devices we're using. If we have very few pins available, we might choose to use serial data. If our microprocessor runs very slowly but has many pins avaiable, we might choose to use parallel data.

For serial data to transmit correct, we need to coordinate when one bit starts and ends. Without the sender and receiver agreeing on this timing, it will be impossible to correctly receive the data. One common method is to use a *periodic signal* (i.e., a square wave) on a separate pin to indicate when a bit starts and ends. This is called a {term}`clock` signal. Each rising edge of the clock signal indicates the start of a new bit. The receiver reads the data pin at each rising edge of the clock signal to get the next bit of data.[^clock]

[^clock]: Clock signals can also be triggers on the falling edge or both edges of a clock signal. The specific timing of the clock signal depends on the communication protocol being used.

How can we control a 7-segment display using serial data when we've seen that it
requires 8 bits of parallel data to simultaneously light all segments? One
approach is to use a device that can convert serial data into parallel data.  A
{term}`shift register` is an example of such a device. A shift register takes in
serial data on one pin and outputs parallel data on multiple pins. By sending
the correct sequence of bits to the shift register, we can control all the
segments of the display using just a few pins on our microcontroller.

### The 74HC595 Shift Register
A very common integrated circuit (IC) that contains a shift register is the
74HC595. The naming is not particularly important for our purposes, but it is
part of a family of chips call the 74xx series, which are widely used in digital
electronics. The *HC* in the name stands for "high speed CMOS", which describes
to electrical engineers what kind of technology was used to build the chip. In
our case, it is worth knowing that *HC* and *HCT* chips will work with the 3.3V
logic levels of our microcontroller, while other chips in the 74xx series may
require 5V logic levels and thus would not be compatible with our
microcontroller. The 595 in the name is the model number of the chip, which in
this case indicates that it contains an 8-bit shift register and a storage
register. Pin 1 of the chip is usually marked with a dot or a notch to indicate the orientation of the chip when placing it on a breadboard. This is important to ensure that we connect the correct pins to our microcontroller and other components.

A diagram showing the pins on the 74HC595 is shown in @fig-74hc595. Pin 8 is
connected to ground and pin 16 is connected to 3.3V to power the chip. Pins 1-7
and 15 are the parallel output pins that we will connect to the segments of our
display. Serial data is provided on pin 14. Pin 13 turns the output of the chip
on or off. Note that the name has a bar over it, which means that it is
{term}`active low`. This means that the output is turned on when this pin is
connected to ground (0V) and turned off when this pin is connected to 3.3V.  It
is also common to see active low signal names labeled with a tilde (~) or an
exclamation mark (!), for example `~OE` or `!OE`. Pins 11 and 12 are pins that
receive clock signals to control when the shift register reads the serial data
and when it updates the parallel output. Pin 10 is used to clear the storage of
the shift register. Pin 9 allows us to connect multiple shift registers together
to control more than 8 bits of parallel data. In fact, we can connect as many
shift registers together as we want to control as many bits of parallel data as
we need, all using the same serial data and clock signals. This is a powerful
feature that allows us to control a large number of devices with just a few pins
on our microcontroller. We won't use it in this book, but it is worth knowing
that this is possible.

```{figure} ./img/74hc595_pinout.svg
:label: fig-74hc595
:alt: Pinout diagram for the 74HC595 shift register integrated circuit
:align: center
Pinout diagram for the 74HC595 shift register integrated circuit. Pins are labeled with their functions.
```

### How a Shift Register Works
A shift register needs two pieces of data to transmit information: the serial data (pin 14) and the clock signal (pin 11). When the clock signal goes from low to high (rising edge), the shift register moves all of the bits it is storing one position to the right and reads the value on the serial data pin into the leftmost position. Each time this happens, the rightmost bit is forgotten since we only have space to store 8 bits. 

```{figure} ./img/shift_register_logic.svg
:label: fig-shift-register-logic
:alt: Diagram showing how a shift register works to convert serial data into parallel data
:align: center
An example of how a shift register works to convert serial data into parallel data. The shift register stores 8 bits of data and shifts them to the right each time a clock signal is received, while reading in new serial data on the leftmost position.
```

### Wiring up the Shift Register
We will modify our parallel circuit in @fig-7segment-parallel-circuit to use a shift register instead. 

Items you will need:
- ESP32 board
- Seven-segment LED display (common cathode)
- 74HC595 shift register IC
- Eight (8) 220Ω resistors
- Large breadboard
- Jumper wires

Wire up the circuit as shown in @fig-7segment-serial-circuit. The shift register
is connected to the seven-segment display with the parallel output pins (1-7 and
15) connected to the segments of the display through 220 Ohm resistors. We then
connect the five control pins of the shift register (pins 10-14) to the
microcontroller.

```{figure} ./img/fig-7segment-serial-circuit.png
:label: fig-7segment-serial-circuit
:alt: Circuit diagram showing how to connect a seven-segment display to an ESP32 microcontroller using a 74HC595 shift register to transmit serial data
:align: center
Circuit diagram showing how to connect a seven-segment display to an ESP32 microcontroller using a 74HC595 shift register. 
```

With this wiring, it is important to note the order that the segments are connected. Notice that segment `A` is connected to `Q_H`. This means that it is attached to the "rightmost" bit of the shift register. 

:::{exercise}
:label: ex-segment-shift-register
Does this mean that the bit for segment `A` should be shifted in first or last when sending serial data to the shift register? 
:::
:::{solution} ex-segment-shift-register
:class: dropdown
Since segment `A` is connected to the rightmost bit of the shift register, it must be shifted in first. By shifting all 8 bits, the bit for segment `A` will end up in the rightmost position, which is where it needs to be to control segment `A`.
:::

We expose all five control signals of the shift register as shown below in @tab-shift-register-pins.

```{table} GPIO Pin Assignments for Shift Register Control
:label: tab-shift-register-pins
:align: center
| Shift Register Pin | Function           | GPIO Pin | Active Level |
|:------------------:|:------------------:|:--------:| :------------:|
| 10                | Clear              | GPIO 27   | Active Low  |
| 11                | Shift Register Clock | GPIO 26  | Rising Edge  |
| 12                | Storage Register Clock | GPIO 25  | Rising Edge  |
| 13                | Output Enable      | GPIO 33   | Active Low  |
| 14                | Serial Data Input  | GPIO 32   | N/A         |
```

### Writing Code to Control the Shift Register
To control the shift register, we first need to define the GPIO pins for the control signals as we did before for the segments of the display.

```{code-block} python
:linenos:
import machine

# Define GPIO pins for shift register control
clear = machine.Pin(27, machine.Pin.OUT)
shift_clock = machine.Pin(26, machine.Pin.OUT)
storage_clock = machine.Pin(25, machine.Pin.OUT)
output = machine.Pin(33, machine.Pin.OUT)
data = machine.Pin(32, machine.Pin.OUT)

# we want to disable clearing the shift register and enable the output by default
clear.on()  # active low, so we set it high to disable clearing
output.off()  # active low, so we set it low to enable output
```

Let's say we'd like to turn on all of the segments of the display. This means that we want to shift in 8 bits of data, all set to 1. We can do this by setting the data pin high and then pulsing the shift clock pin 8 times to shift in the bits.

To make this a bit easier, we can define a function to shift in a bit of data:

```{code-block} python
:linenos:
def shift_in_bit(bit):
    '''
    Shift in a single bit of data to the shift register.
    :param: bit: the bit to shift in (0 or 1)
    '''
    data.value(bit)  # set the data pin to the value of the bit
    shift_clock.on()  # pulse the shift clock to shift in the bit
    shift_clock.off()
```

With this function, we can shift in 8 bits of data to turn on all the segments:

```{code-block} python
:linenos:
# Shift in 8 bits of data, all set to 1, to turn on all
# segments of the display
shift_in_bit(1)
shift_in_bit(1)
shift_in_bit(1)
shift_in_bit(1)
shift_in_bit(1)
shift_in_bit(1)
shift_in_bit(1)
shift_in_bit(1)
```

This alone, unfortunately, will not turn on the segments of the display. The shift register is isolated from the output pins until with explicitly write its contents to the output pins. To do this, we need to pulse the storage clock pin. Let's put this in a function as well:

```{code-block} python
:linenos:
def update_output():
    '''
    Pulse the storage clock to update the output pins with the shifted in data.
    '''
    storage_clock.on()
    storage_clock.off()
```

Putting this all together, we get:

```{code-block} python
:linenos:

import machine

def shift_in_bit(bit):
    '''
    Shift in a single bit of data to the shift register.
    :param: bit: the bit to shift in (0 or 1)
    '''
    data.value(bit)  # set the data pin to the value of the bit
    shift_clock.on()  # pulse the shift clock to shift in the bit
    shift_clock.off()

def update_output():
    '''
    Pulse the storage clock to update the output pins with the shifted in data.
    '''
    storage_clock.on()
    storage_clock.off()

# Define GPIO pins for shift register control
clear = machine.Pin(27, machine.Pin.OUT)
shift_clock = machine.Pin(26, machine.Pin.OUT)
storage_clock = machine.Pin(25, machine.Pin.OUT)
output = machine.Pin(33, machine.Pin.OUT)
data = machine.Pin(32, machine.Pin.OUT)

# Shift in 8 bits of data, all set to 1, to turn on all
# segments of the display
shift_in_bit(1)
shift_in_bit(1)
shift_in_bit(1)
shift_in_bit(1)
shift_in_bit(1)
shift_in_bit(1)
shift_in_bit(1)
shift_in_bit(1)

# Pulse the storage clock to update the output pins with the shifted in data
update_output()
```

:::{exercise}
:label: ex-shift-register-digit
What bit sequence would we need to shift in to display the digit "3" on the seven-segment display? Write code to shift in this bit sequence and update the output to display the digit "3".
:::
:::{solution} ex-shift-register-digit
To display the digit "3" on the seven-segment display, we need to light up
segments A, B, C, D, and G. This corresponds to the bit sequence `01001111`. Recall that segment A is connected to the rightmost bit of the shift register, so we need to shift in the bits in reverse order. Therefore, we would shift in the bits in the following order: 1, 1, 1, 1, 0, 0, 1, 0.

```{code-block} python
:linenos:
# Shift in the bit sequence for the digit "3"
shift_in_bit(1)  # segment A
shift_in_bit(1)  # segment B
shift_in_bit(1)  # segment C
shift_in_bit(1)  # segment D
shift_in_bit(0)  # segment E
shift_in_bit(0)  # segment F
shift_in_bit(1)  # segment G
shift_in_bit(0)  # decimal point
# Update the output to display the digit "3"
update_output()
```
:::

### Other Shift Register Functions
The shift register has a few other functions that we can use. The clear pin (pin 10) can be used to clear the contents of the shift register. This can be useful if we get ourselves into a pickle and just want to reset the shift register to a known state. 

:::{code-block} python
:linenos:
def clear_shift_register():
    '''
    Clear the contents of the shift register.
    '''
    clear.off()  # active low, so we set it low to clear the shift register
    clear.on()   # set it back high to disable clearing
```
:::

The output enable pin (pin 13) can be used to turn the 7-segment display on or off without changing the contents of the shift register. This can be useful if we want to temporarily turn off the display without losing the data we have shifted in. Also, as described in @sec-dimming-led, we can use this pin to create a dimming effect by rapidly turning the display on and off.

```{code-block} python
:linenos:
# replace the output variable assignment with this code to control the output enable pin
output = machine.PWM(machine.Pin(33))
output.freq(1000)  # set the frequency of the PWM signal to 1 kHz
output.duty(512)  # set the duty cycle to 50% to dim the display
``` 

## Additional Exercises

:::{exercise}
Write functions to display the letters `H`, `E`, `L`, `O` on the seven-segment display.

Then write a program that displays `HELLO` on the seven-segment display, pausing
for half a second between each letter.
:::