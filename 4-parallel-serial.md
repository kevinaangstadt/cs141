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
Circuit diagram showing how to connect a seven-segment display to an ESP32 microcontroller. Each segment (a-g) is connected to a separate GPIO pin through a 220 Ohm resistor. The common cathode is connected to ground.
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


## Additional Exercises

:::{exercise}
Write functions to display the letters `H`, `E`, `L`, `O` on the seven-segment display.

Then write a program that displays `HELLO` on the seven-segment display, pausing
for half a second between each letter.
:::