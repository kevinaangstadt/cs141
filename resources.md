---
numbering:
    title: false
---
(resources)=
# Useful Files and Resources

(switch.py-download)=
## `switch.py`
MicroPython does not provide a built-in way to handle switch bounce, but the `switch.py` file here provides a simple way to debounce a switch. 

{button}`Download switch.py <./code/switch.py>`

(lcd_i2c-download)=
## `lcd_i2c` module
The `lcd_i2c` module provides a simple interface for controlling an LCD display using the I2C communication protocol. It includes functions for initializing the display, sending commands and data, and displaying text.

{button}`Download lcd_i2c.zip <./code/lcd_i2c.zip>`

You will need to unzip the downloaded file and copy the entire `lcd_i2c` folder
to the root directory of your MicroPython device in order to use the module in
your programs.

### Usage

Create an LCD object in your code like this:

```{code-block} python
:linenos:

import machine

import lcd_i2c

i2c = machine.I2C(1, sda=machine.Pin(21), scl=machine.Pin(22))
lcd = lcd_i2c.LCD(0x27, 16, 2, i2c=i2c)

# enable the display
lcd.begin()
```

You can then print text to the LCD using the `print` method:

```{code-block} python
lcd.print("Hello, World!")
```

Print understands `\n` for newlines as well as `\c` for centering text on the current line:

```{code-block} python
lcd.print("Hello, \n\cWorld!")
```

You can move the cursor back to the home position (top-left corner) using the `home` method:

```{code-block} python
lcd.home()
```

You can also set a custom cursor position using the `set_cursor` method, which takes a column and row index (both starting at 0):

```{code-block} python
lcd.set_cursor(5, 1)  # move cursor to column 5 of row 1 (second row)
lcd.print("Hello!")
```
