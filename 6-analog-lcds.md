# Analog Inputs and LCDs

In the previous chapter, we introduced the concept of looping. We can now start
to write programs that run forever, and we can use that to read from sensors and
display information while disconnected from a computer. In this chapter, we will
learn how to read from analog sensors and display information on an LCD screen.

## Analog Inputs
So far, we have only considered *digital* signals, which are either on or off.
However, many sensors produce {term}`analog` signals. An analog signal generally
will be a voltage that can take on any value within a certain range, such as
between 0 and 3.3 volts. This is really convenient because we can encode a
significant amount of information in just a single signal, but it is also more
difficult to read when microcontrollers are designed for digital signals. 

Microcontrollers often have a special component called an *analog to digital
converter* (ADC) that can read an analog signal and convert it to a digital
value that we can use in our programs. MicroPython gives us a simple was to read
this pin value and get its equivalent value in microvolts (a microvolt is one
millionth of a volt).

Not all pins on the microcontroller can be used for analog input, so we must
select a pin that has an ADC associated with it. On the ESP32, the pins that can
be used for analog input are 0, 2, 4, 12-15, 25-27, and 32-39. We can create an
`ADC` object for one of these pins and then call the `read_u16()` method to get
a value in the range 0-65535.

What does this number represent? This number is a *relative* value that
represents the voltage on the pin as a fraction of the maximum voltage that the
ADC can read. For example, if the ADC can read voltages up to 3.3 volts, then a
reading of 32768 would represent a voltage of approximately 1.65 volts (half of
3.3 volts).

One major consideration is that the ADC on the ESP32 can only read voltages up
to around 1.1 volts directly, so if we want to read a sensor that produces a
higher voltage, we need to {term}`attenuate` the signal. Fortunately,
MicroPython provides a simple way to do this by calling the `atten()` method on
the `ADC` object. For example, if we want to read a sensor that produces
voltages up to 3.3 volts, we can call `adc.atten(machine.ADC.ATTN_11DB)` to set
the attenuation level to 11 decibels, which allows us to read voltages up to 3.3
volts.

As a complete example, to read from pin 34, we can do the following:

```{code-block} python
:linenos:

import machine
adc = machine.ADC(machine.Pin(34, machine.Pin.IN))
adc.atten(adc.ATTN_11DB)

while True:
    value = adc.read_u16()
    print(value)
```

:::{note}

It's worth noting that the ADC on the ESP32 is not known for being very
accurate, and the readings can be quite noisy. If you need more accurate
readings, you may want to consider using an external ADC that connects to the
microcontroller via serial communication, such as I2C or SPI. These external
ADCs often have better resolution and accuracy than the built-in ADC on the
ESP32.

:::

There is also a `read_uv()` method that returns the voltage in microvolts, which can be more convenient for some applications. This method tries to account for manufacturing variations in the ADC and provide a more accurate voltage reading. There can still be a decent amount of error in these readings, which can have an impact on the accuracy of our sensor readings, but it is generally better than using the raw `read_u16()` values.

## Reading Temperature with a Thermistor
A common type of analog sensor is a {term}`thermistor`, which is a type of resistor that changes its resistance based on the temperature. By measuring the voltage across the thermistor, we can determine the temperature. A common type of thermistor is the NTC (negative temperature coefficient) thermistor, which decreases its resistance as the temperature increases. 

A thermistor's resistance follows a specific mathematical relationship with
temperature, which can be described by the [Steinhart-Hart
equation](https://en.wikipedia.org/wiki/Steinhart–Hart_equation).
To calculate the temperature from the resistance thermistor, we need to know *B-Parameter* value of the thermistor, which is a constant that describes how the resistance changes with temperature. This value is specific to the particular thermistor we are using and can usually be found in the datasheet. 

Additionally, we need to know the resistance of the thermistor $R_0$ at a
reference temperature $T_0$, which is typically 25 degrees Celsius (298.15
Kelvin). For a thermistor labeled `103`, the $R_0$ value is 10000 ohms. With
these values, we can calculate the resistance of the thermistor at any given
temperature (in Kelvin) using the following formula:

$$T = \frac{T_0 * B}{T_0 \ln\left(\frac{R}{R_0}\right) + B}$$

:::{exercise}
:label: thermistor-calc

Calculate the temperature in Celsius for a thermistor with a B-Parameter of 3950, an $R_0$ value of 10000 ohms at 25 degrees Celsius, and a measured resistance of 5000 ohms.
:::
:::{solution} thermistor-calc

$$
\begin{align*}
T &= \frac{T_0 * B}{T_0 \ln\left(\frac{R}{R_0}\right) + B} \\
  &= \frac{298.15 * 3950}{298.15 \ln\left(\frac{5000}{10000}\right) + 3950} \\
  &\approx \frac{1182747.5}{-206.66 + 3950} \\
  &\approx \frac{1182747.5}{3743.34} \\
  &\approx 315.96 \text{ Kelvin} \\
\end{align*}
$$

Since we know that 0 degrees Celsius is equal to 273.15 Kelvin, we can convert the result back to celsius by subtracting 273.15 from the result in Kelvin: $315.96 - 273.15 = 42.81^\circ C$.
:::

### Converting Voltage to Resistance
The astute reader will note that an analog pin reads *voltage*, not
*resistance*. Thus the equation above is not directly useful for calculating the
temperature from the value read from the ADC. Fortunately, we can use a clever
trick to convert the resistance of the thermistor to a voltage that we can read
from the ADC. We do this by creating a {term}`voltage divider` circuit.

A voltage divider is a simple circuit that uses two resistors between a high voltage (like 3.3 volts) and ground. The voltage between the two resistors and ground will be a known fraction of the high voltage, and that fraction depends on the values of the two resistors. If we use the thermistor the resistor between the midpoint and ground in the voltage divider, we can calculate the voltage at the midpoint of the divider using the following formula:

$$ V_{out} = V_{in} \cdot \frac{R_{thermistor}}{R_1 + R_{thermistor}} $$

$V_{out}$ is the voltage we read with the microcontroller, $V_{in}$ is the high
voltage (3.3 volts), $R_{thermistor}$ is the resistance of the thermistor, and
$R_1$ is the resistance of the other resistor in the voltage divider. We
typically choose $R_1$ to be the same as the resistance of the thermistor at
room temperature (10,000 ohms in this case) to maximize the sensitivity of the
voltage divider around room temperature.

With some basic algebra and plugging in our known values, we can rearrange the
formula to solve for $R_{thermistor}$ in terms of $V_{out}$:

$$ R_{thermistor} = 10000 \cdot \frac{V_{out}}{3.3 - V_{out}} $$

With this formula, we are now set to read the temperature from the thermistor by first reading the voltage from the ADC, converting that voltage to resistance using the formula above, and then converting that resistance to temperature using the Steinhart-Hart equation!

### Wiring up the Circuit
To connect the thermistor to the microcontroller, we will need to construct a
voltage divider circuit and connect it to an appropriate pin on the
microcontroller. 

Items you will need:
* ESP32 board
* Thermistor (possibly a black round device with two leads coming out of it, labelled `103`)
* 10KΩ resistor
* Mini breadboard
* Jumper wires

Wire up the circuit as shown in @fig-thermistor-circuit. We are connecting the
thermistor to GPIO 14.

```{figure} /img/fig-thermistor.png
:label: fig-thermistor-circuit
:alt: Wiring diagram for connecting a thermistor to an ESP32 using a voltage divider circuit. This image was created using Fritzing.
:align: center
Wiring diagram for connecting a thermistor to an ESP32 using a voltage divider circuit. This image was created using [Fritzing](http://fritzing.org/).
```

### Writing the Code
Now that we have the circuit wired up, we can write the code to read the temperature from the thermistor. We will use the `math` module to perform the logarithmic calculations needed for the Steinhart-Hart equation. By default, `math.log()` computes the natural logarithm, which is what we need for the equation. 

```{code-block} python
:linenos:
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

# constants for the thermistor
B = 3950    # A typical B-Parameter value for an NTC thermistor
R0 = 10000  # 10K ohms at 25 degrees Celsius
T0 = 298.15 # 25 degrees Celsius in Kelvin

# loop forever and print the temperature every second
while True:
    # call our function to read the temperature
    temperature = read_temperature(thermistor, B, R0, T0)
    # Print the temperature rounded to 2 decimal places
    print(f"Temperature: {round(temperature, 2)} C")
    # wait for 1 second before reading again
    time.sleep(1)
```

:::{note}

We noted that the accuracy of the ADC can be quite poor, which can lead to
inaccurate temperature readings. Because we're not trying to measure large
temperature changes, we could try to improve this by adding a *correction factor* to our initial voltage reading to account for the error in the ADC. 

To do this, add a `print` statement to output `V_thermistor` to the console.
Using a digital multimeter, measure the actual voltage between ground and the pin connected to the thermistor as shown in @fig-thermistor-multimeter. Compare this voltage to the value printed by the code. 

Add a line to calculate the correction factor as the ratio of the actual voltage to the measured voltage, and then multiply `V_thermistor` by this correction factor before using it in the rest of the calculations. This should help improve the accuracy of our temperature readings.

The beginning of our function would now look like this:

```{code-block} python
:linenos:
:lineno-start: 14
    # calculate the correction factor
    CORRECTION_FACTOR = <actual_voltage> / <printed_voltage>
    # read the ADC value in microvolts and convert it to volts
    V_thermistor = thermistor.read_uv() / 1000000 * CORRECTION_FACTOR
```

```{figure} /img/fig-thermistor-multimeter.png
:label: fig-thermistor-multimeter
:alt: A photo of a multimeter measuring the voltage across the thermistor in the circuit.
:align: center
A photo of a multimeter measuring the voltage across the thermistor in the circuit.
```

:::

## Using an External Display
Printing to the console is useful for debugging, but it is not very practical
for a standalone device. To display information in a more user-friendly way, we
can use an external display. One common type of display is an LCD (liquid
crystal display), which can show text (and sometimes simple graphics). We will
use a very popular LCD that can display 2 lines of text with 16 characters per
line, often referred to as a "16x2 LCD". A popular version of this LCD display uses serial communication to send data from the microcontroller to the display.

In @chap-parallel-serial, we learned that serial communication needs both a data
line and a clock line to synchronize the data transfer. In the past examples, we
used a technique called {term}`bit-banging` to manually toggle the data and
clock lines in our code to send data to the display. However, this can be
inefficient and can cause timing issues if our code is doing other things at the
same time.

The LCD controller supports a serial protocol called I2C (pronounced "eye-squared-see" or "eye-two-see"), which MicroPython knows how to "speak" natively. We just have to wire up the data (SDA) and clock (SCL) pins to GPIO 21 and 22 respectively, and then we can use the built-in `machine.I2C` function to create an I2C object that we can use to communicate with the LCD. We will also need to install a library that provides a convenient interface for controlling the LCD. You can download this from @resources.

We can actually wire multiple I2C devices to the same data and clock lines. Each
device has a unique address that allows MicroPython to communicate with each
device individually. This means that we can easily add more sensors or displays
to our project without needing to use additional pins on the microcontroller, as
long as those devices also support I2C communication.

The LCD display we are using has an I2C address of 0x27, which is the default address for many I2C LCD displays. If you have a different LCD display, you may need to check the documentation to find the correct I2C address.

### Wiring up the LCD
Let's add the LCD to our circuit. The LCD is designed to be powered by 5 volts,
so we will connect the VCC pin to the 5V pin on the ESP32. 

Additional items you will need:
* 16x2 LCD display with I2C interface
* Jumper wires

Wire up the LCD as shown in @fig-lcd-thermistor-circuit. The SDA and SCL pins of the LCD should be connected to GPIO 21 and 22 respectively.

```{figure} /img/fig-lcd-thermistor.png
:label: fig-lcd-thermistor-circuit
:alt: Wiring diagram for connecting a 16x2 LCD display with I2C interface to an ESP32 already wired for a thermistor. This image was created using Fritzing.
:align: center
Wiring diagram for connecting a 16x2 LCD display with I2C interface to an
ESP32. This is in addition to a thermistor. This image was created using [Fritzing](http://fritzing.org/).
```

### Writing the Code
Now that we have the LCD wired up, we can modify our code to display the temperature on the LCD instead of printing it to the console. We will use the `lcd_i2c` module that we downloaded from @resources to control the LCD. This module provides a simple interface for initializing the display, sending commands and data, and displaying text.

```{code-block} python
:linenos:
import machine
import math
import time

# NEW import the lcd_i2c module
import lcd_i2c

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

# NEW set up the I2C connection and initialize the LCD
i2c = machine.I2C(1, sda=machine.Pin(21), scl=machine.Pin(22))
lcd = lcd_i2c.LCD(0x27, 16, 2, i2c=i2c)
lcd.begin()

# set up the ADC on pin 14
thermistor = machine.ADC(machine.Pin(14, machine.Pin.IN))
thermistor.atten(thermistor.ATTN_11DB)

# constants for the thermistor
B = 3950    # A typical B-Parameter value for an NTC thermistor
R0 = 10000  # 10K ohms at 25 degrees Celsius
T0 = 298.15 # 25 degrees Celsius in Kelvin

# loop forever and print the temperature every second
while True:
    # call our function to read the temperature
    temperature = read_temperature(thermistor, B, R0, T0)
    # NEW Display the temperature on the LCD
    # by moving the cursor to the home position, we overwrite the previous 
    # temperature reading on the LCD instead of printing a new line each time
    lcd.home()
    lcd.print(f"Temp: {round(temperature, 2)} C")
    # wait for 1 second before reading again
    time.sleep(1)
```

:::{warning}
There is actually a bug in the code above! Can you spot it? 

Because we are overwriting the previous temperature reading on the LCD, if the new temperature reading has fewer characters than the previous reading, we will end up with leftover characters from the previous reading on the display. For example, if the first reading is "Temp: 25.00 C" and the second reading is "Temp: 5.00 C", the display will show "Temp: 5.00 CC" because the "C" from the first reading is not overwritten by the second reading.

We can fix this by adding some extra spaces at the end of the string we print to the LCD to ensure that we overwrite any leftover characters from the previous reading. For example, we can change the line that prints to the LCD to:

```python
# add extra spaces to overwrite leftover characters
lcd.print(f"Temp: {round(temperature, 2)} C   ")  
```
:::

## Running the Code on Boot
It would be really cool to walk around with our device and have it display the
temperature without needing to connect it to a computer and run the code
manually. 

When powered on, MicroPython automatically looks for and runs a file named
`main.py` on the device. We can take advantage of this in combination with an
`import` statement to run our code on boot.

First, copy your python file for the thermistor and LCD code to the device. Let's assume you've named it `thermistor_lcd.py`. Then create a new file named `main.py` on the device with the following content:

```{code-block} python
import thermistor_lcd
```

Why does this work? When `main.py` is run on boot, it imports the
`thermistor_lcd` module, which executes all the code in `thermistor_lcd.py`.
Since our `thermistor_lcd.py` file contains a *Main Program*, it will execute on
import and start reading the temperature and displaying it on the LCD
immediately after the device is powered on.

Now, any time you power on the device, it will automatically start running the
code to read the temperature from the thermistor and display it on the LCD
without needing to connect it to a computer and run the code manually. To
disable this, just delete the `main.py` file from the device or change its
contents to not import the `thermistor_lcd` module. This way, you don't lose the
code you wrote, but it just won't run on boot.

## Additional Exercises

:::{exercise}
:label: thermistor-voltage-practice-1
Calculate the voltage output from the voltage divider circuit when the 
thermistor is at room temperature (25 degrees Celsius) and has a resistance of 
10,000 ohms. Assume the input voltage is 3.3 volts and the other resistor in the 
voltage divider is also 10,000 ohms.
:::

:::{exercise}
:label: thermistor-voltage-practice-2
Calculate the voltage output from the voltage divider circuit when the 
thermistor is at 50 degrees Celsius and has a resistance of 3,162 ohms. Assume 
the input voltage is 3.3 volts and the other resistor in the voltage divider is 
10,000 ohms.
:::

:::{exercise}
:label: thermistor-temperature-practice-1
Calculate the temperature in Celsius for a thermistor with a B-Parameter of 
3950, an $R_0$ value of 10000 ohms at 25 degrees Celsius, and a measured 
resistance of 1250 ohms.
:::

:::{exercise}
:label: thermistor-temperature-practice-2
Calculate the temperature in Celsius for a thermistor with a B-Parameter of 
3950, an $R_0$ value of 10000 ohms at 25 degrees Celsius, and a measured 
resistance of 9875 ohms.
:::

:::{exercise}
:label: thermistor-average
The temperature readings from the thermistor can be noisy due to fluctuations in the voltage. Modify your code to take an average of 10 readings taken 100 milliseconds apart to get a more stable temperature reading.
:::

:::{exercise}
:label: thermistor-fahrenheit
Modify your code to also print the temperature in degrees Fahrenheit. Don't just embed the conversion, but use a separate function to convert from Celsius to Fahrenheit. The formula for converting Celsius to Fahrenheit is: $F = C \cdot \frac{9}{5} + 32$. (You might even have this function already!)
:::