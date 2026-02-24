# Binary Numbers and Repetition

As we saw in the previous chapter, each pin of the microcontroller can output a
binary digit (a bit), better known as a 0 or a 1. We can combine these bits to
represent more complex information, such as the segments of a display. For more
complex operations, we are going to need additional programming power to control
the pins. In this chapter, we will learn how to use loops to repeat a block of
code multiple times, which is essential for tasks like counting in binary or
controlling multiple pins efficiently.

## Binary Numbers
At its most basic level everything about modern computing boils down to, at some
base level, ones and zeros, true/false, on/off, yes/no, black/white. All
information is *binary*. All decimal (base-10) numbers are expressed in binary
(base-2). Digital images are just numbers, which are binary. Digital music on
Spotify or Pandora, are numbers (hence binary) that represent sampled sound
waves. Characters, letters, punctuation, all have a numeric equivalent, and are
binary. Even computer programs get converted to binary. *All information is
binary*.

We previously saw that a group of eight bits is called a byte. In modern
computing, we often work with thousands, millions, or even billions of bytes of
data at a time. @tab-size-data shows common prefixes for large data sizes.
Strictly speaking, we should be using the binary prefixes (kibi, mebi, gibi,
etc.) for data sizes, but in practice, the decimal prefixes (kilo, mega, giga)
are often used interchangeably as they are close enough in value for most
practical purposes.

```{table} Sizes of data
:label: tab-size-data
:align: center

| Size Term      | Base-10 Power         | Base-2 Power       |
|:---------------|:----------------------|:-------------------|
| Kilobyte (KB)  | $10^3 = 1{,}000$      | $2^{10} = 1{,}024$ |
| Megabyte (MB)  | $10^6 = 1{,}000{,}000$| $2^{20} = 1{,}048{,}576$ |
| Gigabyte (GB)  | $10^9$                | $2^{30}$           |
| Terabyte (TB)  | $10^{12}$             | $2^{40}$           |
| Petabyte (PB)  | $10^{15}$             | $2^{50}$           |
| Exabyte (EB)   | $10^{18}$             | $2^{60}$           |
```

### Converting from Base-2 to Base-10
What does the number `123` mean in decimal or base-10? When we see something
like this, our brain immediately reads it as one hundred twenty-three. But what
does it actually mean? The number `123` is a shorthand for the sum of the
following: $$ 3 \times 10^0 + 2 \times 10^1 + 1 \times 10^2 $$ Colloquially, we
say that 3 is in the "ones place", 2 is in the "tens place", and 1 is in the
"hundreds place". The value of each digit is determined by its position in the
number. Each place is offset by a power of ten.

We can do the exact same thing with binary numbers, except each place is now a
power of two instead of ten. Thus, the initial set of places would be the "ones
place" (2^0), the "twos place" (2^1), the "fours place" (2^2), the "eights
place" (2^3), and so on. For example, the binary number `1011` can be converted
to decimal as follows: $$ 1 \times 2^0 + 1 \times 2^1 + 0 \times 2^2 + 1 \times
2^3 = 1 + 2 + 0 + 8 = 11 $$ Therefore, the binary number `1011` is equal to the
decimal number `11`.

```{exercise}
:label: ex-binary-conversion

Convert the following binary numbers to decimal:
1. `1101`
2. `10010`
3. `11111111`
```
```{solution} ex-binary-conversion
:class: dropdown
1. 13
2. 18
3. 255
```

### Converting from Base-10 to Base-2
Going the opposite direction is a little more complicated, but it can be done
using a method called "repeated division". To convert a decimal number to
binary, we repeatedly divide the number by 2 and keep track of the remainders.
The binary representation is then formed by reading the remainders in reverse
order.

```{exercise}
:label: ex-decimal-binary-operations
What two MicroPython operators can we use to get the quotient and remainder when dividing by 2?
```
```{solution} ex-decimal-binary-operations
:class: dropdown
The `//` operator gives the quotient (integer division), and the `%` operator gives the remainder (modulo).
```

Let's convert the decimal number `13` to binary using repeated division:
1. Divide 13 by 2: quotient = 6, remainder = 1
2. Divide 6 by 2: quotient = 3, remainder = 0
3. Divide 3 by 2: quotient = 1, remainder = 1
4. Divide 1 by 2: quotient = 0, remainder = 1
Now we read the remainders in reverse order: `1101`. Therefore, the decimal number `13` is equal to the binary number `1101`.

```{exercise}
:label: ex-decimal-to-binary
Convert the following decimal numbers to binary:
1. 5
2. 56
3. 245
```
```{solution} ex-decimal-to-binary
:class: dropdown
1. `101`
2. `111000`
3. `11110101`
```

### Hexadecimal Numbers
Decimal numbers a nice because we're used to counting on our ten fingers and
toes, but they aren't super convenient for converting to and from binary. Binary
is also a pain because numbers get very long, very quickly. It turns out that having more than two digits has its perks! If we choose a number of digits that is a power of two, we can easily convert between that base and binary.

The next power of two after 10 is 16, which means that if we use 16 digits, we can easily convert between that base and binary. {term}`Hexadecimal` numbers use 16 digits: 0-9 and A-F, where A represents 10, B represents 11, C represents 12, D represents 13, E represents 14, and F represents 15. Each hexadecimal digit corresponds to four binary digits (bits), which makes it a convenient way to represent binary data in a more compact form.

@tab-size-hexadecimal shows the hexadecimal digits and their corresponding decimal and binary values. To help distinguish between hexadecimal, decimal, and binary numbers, we often use prefixes: `0x` for hexadecimal, `0b` for binary, and no prefix for decimal. 

```{table} Hexadecimal Digits
:label: tab-size-hexadecimal
:align: center
| Hexadecimal Digit | Decimal Value | Binary Value |
|:------------------|:--------------|:-------------|
| 0x0                | 0             | 0b0000        |
| 0x1                | 1             | 0b0001        |
| 0x2                | 2             | 0b0010        |
| 0x3                | 3             | 0b0011        |
| 0x4                | 4             | 0b0100        |
| 0x5                | 5             | 0b0101        |
| 0x6                | 6             | 0b0110        |
| 0x7                | 7             | 0b0111        |
| 0x8                | 8             | 0b1000        |
| 0x9                | 9             | 0b1001        |
| 0xA                | 10            | 0b1010        |
| 0xB                | 11            | 0b1011        |
| 0xC                | 12            | 0b1100        |
| 0xD                | 13            | 0b1101        |
| 0xE                | 14            | 0b1110        |
| 0xF                | 15            | 0b1111        |
```

## Encoding Seven-Segment Display Values
Now that we understand how to convert between binary and decimal, we can use
this knowledge to control the seven-segment display more efficiently. Instead of
writing out individual bits for each segment as we did in the previous chapter,
we can store the encoding as two hexadecimal digits, which is much more compact and easier to read in our code.

Suppose, for example, we wish to display the digit `0`, which requires segments A through F to be on and segments G and the DP to be off. We would need to insert `0b00111111` into the shift register to achieve this.

```{exercise}
:label: ex-seven-segment-hex
What is the hexadecimal representation of the binary number `0b00111111`?
```
```{solution} ex-seven-segment-hex
We can split the binary number into two groups of four bits: `0011` and `1111`. The first group `0011` corresponds to the hexadecimal digit `3`, and the second group `1111` corresponds to the hexadecimal digit `F` (use @tab-size-hexadecimal). Therefore, the hexadecimal representation of `0b00111111` is `0x3F`.
```

Now, we just need some code that can take our hexadecimal encoding and convert it to the appropriate binary signals to control the shift register. We can use the same repeated division method we used for converting decimal to binary to convert hexadecimal to binary.

The code for this might look a little something like this:

```{code-block} python
:linenos:

def output_value(value):
    """
    Output the value as a sequence of bits to the
    shift register
    :param value: number that can be represented with 8 bits
    """
    # do the following 8 times

    # shift out the bit that is the result of value % 2
    # this will be 0 or 1 and the smallest bit of the value (the "ones place")
    shift_in_bit(value % 2)
    # divide the value by 2 to remove the bit we just output
    value = value // 2
    
    # shift out the bit that is the result of value % 2
    shift_in_bit(value % 2)
    # divide the value by 2 to remove the bit we just output
    value = value // 2
    
    # shift out the bit that is the result of value % 2
    shift_in_bit(value % 2)
    # divide the value by 2 to remove the bit we just output
    value = value // 2
    
    # shift out the bit that is the result of value % 2
    shift_in_bit(value % 2)
    # divide the value by 2 to remove the bit we just output
    value = value // 2
    
    # shift out the bit that is the result of value % 2
    shift_in_bit(value % 2)
    # divide the value by 2 to remove the bit we just output
    value = value // 2
    
    # shift out the bit that is the result of value % 2
    shift_in_bit(value % 2)
    # divide the value by 2 to remove the bit we just output
    value = value // 2
    
    # shift out the bit that is the result of value % 2
    shift_in_bit(value % 2)
    # divide the value by 2 to remove the bit we just output
    value = value // 2
    
    # shift out the bit that is the result of value % 2
    shift_in_bit(value % 2)
    # since we alread output 8 bits, we don't need to divide the value by 2 again
```

Notice how much repetition there is in this code. We are doing the same thing
eight times, just with a different value stored in a variable each time. In
computer science, there is a common principle called "Don't Repeat Yourself"
(DRY), which encourages us to avoid writing the same code multiple times.  The
problem with repeating yourself is that it can lead to errors and makes your
code harder to maintain. If you need to change something in the repeated code,
you have to remember to change it in every place it appears, which can be
error-prone.

Fortunately, there is a programming language construct designed specifically to repeat lines of code multiple times.

## The `while` Loop
The `while` loop repeats a body of code (indented) as long as some condition is `true`. The syntax is as follows:

```{code-block} python
:linenos:
:emphasize-lines: 1
while 〈condition〉:
    # body of code to repeat
    code_statement(s)
```

As long as `〈condition〉` remains `true`, MicroPython will execute the entire
body (indented part) of the code. MicroPython will then check the condition
again, and if it is still `true`, it will repeat the body of code again. This
process continues until the condition becomes false.

### Boolean Data and Relational Operators
The `while` loop relies on a condition that is either true or false. That means
we'll need a type of data that can represent true and false values. In
MicroPython, this type is called `bool`, named after the mathematician George
Boole who studied logic. A `bool` can have one of two values: `True` or `False`. 

:::{tip}
`True` and `False` in MicroPython (with capital `T`and `F`) are literal values in the programming language, just like `1` and `0` are literal values for integers. They are not strings, so they should not be enclosed in quotes. They are also not variables, so they should not be used as variable names. However, you can you can save a `bool` value in a variable, just like you can save an integer or a string in a variable.
:::

Much like we have arithmetic operators for working with numbers, we have *relational operators* for working with boolean values as shown in @tab-relational-operators. These operators allow us to compare values and produce a boolean result that can be used as the condition for a `while` loop.

```{table} Relational Operators
:label: tab-relational-operators
:align: center

| Operator   | Description            |
|:-----------|:-----------------------|
| `<`        | Less than              |
| `<=`       | Less than or equal to  |
| `>`        | Greater than           |
| `>=`       | Greater than or equal to |
| `==`       | Equal to               |
| `!=`       | Not equal to           |
```

### Counting Loops
We need to perform our repeated division process 8 times to convert a hexadecimal value to binary. How can we make a `while` loop that executes exactly 8 times? This is a common task in programming, and there is a common template we use called a counting loop. A counting loop uses a variable to keep track of the current execution number.

Say we wish to count from `start` to `end`. The basic structure of a counting loop is as follows:

```{code-block} python
:linenos:
counter = start
while counter <= end:
    # body of code to repeat
    code_statement(s)
    # ... more code statements if needed

    # IMPORTANT! Update the counter variable to the next value
    counter = counter + 1
``` 

In our case, we want to count from `1` to `8`, so we can set `start` to `1` and `end` to `8`. The body of the loop will contain the code for performing one step of the repeated division process. After executing the body of the loop, we update the counter variable to move on to the next execution number. This way, we can ensure that the loop executes exactly 8 times.

```{code-block} python
:linenos:
counter = 1
while counter <= 8:
    # calculate the bit to shift out based on the current value
    shift_in_bit(value % 2)
    # divide the value by 2 to remove the bit we just output
    value = value // 2

    # update the counter variable to the next value
    counter = counter + 1
```

Putting this all together, we can rewrite our `output_value` function using a `while` loop to avoid repetition:

```{code-block} python
:linenos:
def output_value(value):
    """Output the value as a sequence of bits to the
    shift register
    :param value: number that can be represented with 8 bits
    """
    counter = 1
    while counter <= 8:
        # calculate the bit to shift out based on the current value
        shift_in_bit(value % 2)
        # divide the value by 2 to remove the bit we just output
        value = value // 2

        # update the counter variable to the next value
        counter = counter + 1
```

:::{exercise}
:label: ex-counting-loop-table

Print a table of powers of two up to $2^{10}$.

```
i   2^i
==========
0  | 1
1  | 2
2  | 4
3  | 8
...
10 | 1024
----
```
:::
:::{solution} ex-counting-loop-table
We can use a counting loop to print the table of powers of two. We will need to count from `0` to `10`, and for each value of `i`, we will calculate `2^i` and print it in the desired format.

```{code-block} python
:linenos:
# table header
print("i     2^i")
print("=========")

i = 0                       
while i <= 10:
    # print the current value of i and 2^i in the desired format
    print(i, '\t|', 2**i)
    # update the counter variable to the next value
    i = i + 1              
```

By convention, we often use `i`, `j`, and `k` as variable names for counters in
counting loops, but you can use any variable name you like. 

As an alternative to `i <= 10`, we could also use `i < 11` as the loop
condition, which would achieve the same result. 

The `\t` in the `print` statement is a tab character that helps to align the
columns of the table. This helps us line up the numbers in a neat format, making
it easier to read the table. 
:::

:::{exercise}
:label: ex-counting-loop-bug

What would happen if we forgot to update the counter variable in the previous
exercise?
:::
:::{solution} ex-counting-loop-bug

If we forget to include this step, the loop will run indefinitely because the
condition will always be true. This is a common mistake when writing loops, and
it can lead to programs that never stop running, which is why it's important to
always remember to update the counting variable in a counting loop.

:::

### Accumulating Loops
Another common loop pattern is to keep a running total. For example, computing
the sum of the integers from $1$ to $n$. That is, $1 + 2 + 3 + \cdots + n$ where $n$ is entered by the user.[^summation]

[^summation]: forgetting for the moment that there is a closed form answer of
    $\frac{n(n+1)}{2}$ 

We can develop a template for this type of loop, which we will call an *accumulating loop* because we are accumulating a total as we go. The structure of an accumulating loop is as follows:

```{code-block} python
:linenos:
# create a variable to hold the total and initialize it to 0
# if we are computing a product instead of a sum, we would initialize 
# this variable to 1 instead of 0
total = 0

# create a counter variable to keep track of the current execution number 
# and initialize it to the starting value
counter = start

while counter <= end:
    # body of code to repeat
    code_statement(s)
    # ... more code statements if needed

    # do something to update the total variable based on the current 
    # value of counter or other data

    # update the counter variable to the next value
    counter = counter + 1
```

For our specific example of computing the sum of the integers from `1` to `n`, we can set `start` to `1` and `end` to `n`. The body of the loop will contain the code for adding the current value of `counter` to the `total`. After executing the body of the loop, we update the counter variable to move on to the next integer.

```{code-block} python
:linenos:

# ask for user input and convert it to an integer
n = int(input("Enter n: "))  

# create a variable to hold the total and initialize it to 0
total = 0

# create a counter variable to keep track of the current execution number and
# initialize it to the starting value
i = 1

while i <= n:
    # add the current value of counter to the total
    total = total + i

    # update the counter variable to the next value
    i = i + 1

print(f"The sum of the integers from 1 to {n} is {total}.")
```

In this code, we purposefully avoided the variable name `sum` for the total because `sum` is a built-in function in MicroPython. Looking at the line `total = total + i`, it is best to interpret this using the prhasing we suggest for assignment statements: *the new value of `total` gets the old value of `total` plus `i`*.

:::{tip} 

Programmers often use assignment statements such as `x = x + 1`. Most
programming languages, MicroPython included, has a `+=` operator and we can
write `x = x + 1` as the more pithy `x += 1`.[^in-place] 

[^in-place]: The operator `+=` is really called the *in place add* operator and
    can have a different behavior than one might expect.

The while loop in the example above could be rewritten to be 
```{code-block} python
:linenos:
while i <= n:                   
    total += i               
    i += 1                   
```

:::

:::{exercise}
:label: ex-accumulating-loop-average

Write a program that computes the average of non-negative numbers (e.g., quiz
grades) entered by the user. Quit reading numbers when the user has entered a
negative number. Be careful, make sure you don’t include the negative number in
the average. Here is an example run of the program.

```
Enter a number: 3
Enter a number: 9
Enter a number: 7
Enter a number: 8
Enter a number: -1
The average is  6.75
```
:::
:::{solution} ex-accumulating-loop-average
:class: dropdown
Here is one solution to the problem:
```{code-block} python
:linenos:
n = float(input("Enter a number: "))
i = 0
total = 0

while n >= 0:
    i += 1
    total += n
    n = float(input("Enter a number: "))

average = total / i
print("The average is ", round(average, 2))
```

This is actually a little tricky. Notice the first line. We read our first
number *before* the loop. Once we get into the loop we know that we must have
entered a non-negative number.

There is actually a subtle bug in this code that can sometimes lead to a crash. Can you find it?[^bug]

[^bug]: Hint: What if the very first number the user entered was negative?
:::

### Infinite Loops
With microcontrollers, it is quite common to have a program that runs forever,
or at least until the power is turned off. For example, we may wish to
continuously output a message to a display, or continuously read sensor data and
respond to it. 

In all of our previous programs, MicroPython would execute the code and then
stop. We can create a program that runs indefinitely by using a `while` loop
with a condition that is always `True`. In this case, we can use the boolean
literal `True` as the condition for the loop, which will cause it to run
forever.

```{code-block} python
:linenos:
# This program will never terminate
# it will just keep (re)executing the loop body forever
while True:
    # body of code to repeat indefinitely
    code_statement(s)
    # ... more code statements if needed

# code here will never be reached because the loop runs forever
print("This will never be printed.")
```

We call this an *infinite loop* because it runs indefinitely. Infinite loops are
useful for microcontroller programs that need to run continuously, but they can
also be a source of bugs if not used carefully. If you accidentally create an
infinite loop in a program that is not meant to run forever, it can cause your
computer to become unresponsive or crash. 

:::{note}

For something as simple as `while True`, it's possible to notice this is an
infinite loop just by looking at the code. However, it turns out that it is
impossible to always determine correctly whether a given program will terminate
or run forever. This is known as the *Halting Problem* and is a fundamental
result in computer science that has implications for software development and
the limits of computability.

:::

## Applications of Loops
Loops are incredibly powerful and useful in programming. They allow us to perform repetitive tasks without having to write the same code multiple times. Here are a couple of applications where loops help us solve problems more efficiently.

### Exponential Growth: Password Length

Why are longer passwords better than shorter passwords? For one, longer
passwords are harder to guess. But how much harder? Let's say we allowed
passwords to contain 26 upper or lower case characters (that is 52 possible
alphabetic characters, in the English alphabet), ten digits 0 through 9, and 32
symbol characters `~!@#$%^&*()_-+={[}]"':;>.<,?/|\`. That is 94 possible
distinct characters that can be used in a password.[^arbitrary-94]

[^arbitrary-94]: A rather arbitrary number, 94, but it is probably close.

There are $94$ one character passwords, $94^2 = 8836$ two character passwords,
$94^3 = 830584$ three character passwords, and so on, so that if a password was
ten characters long there are $94^{10} = 53861511409489970176$ possible
passwords or approximately $5 \times 10^{19}$.

Plotting $94^i$, where $i$ is the number of characters in the password, gives us
the graph:

```{figure} ./img/fig-94_to_the_i.png
:label: fig-94_to_the_i
:align: center
:alt: Graph of 94^i
A plot of $94^i$ where $i$ is the number of characters in the password.
```

This is an example of *exponential growth* in the number of characters in the
password. Notice how the graph explodes at between 8 and 10 characters (was it
ever suggested that you make your passwords more than 8 characters long?) What
is the total number of passwords up to 10 characters long? We would have to
include all of the nine character passwords, and the eight character passwords,
etc. and compute the sum $94^1 + 94^2 + 94^3 + \cdots + 94^{10}$.

```{code-block} python
:linenos:

i = 1
total = 0
while i <= 10:
    total += 94**i
    i += 1

print(total)
```

which would print `54440667446151152650`, which is also just bigger than $5.4 \times 10^{19}$.

To emphasize the difference between a six character password and a ten character
password, let's assume a malicious hacker was trying to break into a system by
trying all possible passwords. How long might it take? Let's say we had a
powerful computer that could attempt 1 billion passwords per second.

For a six character password that's $94^6/10^9/60 \approx 11.5$ minutes to try
all possibilities. On average we will search about half the passwords, so on
average it would take about $6$ minutes.

For a ten character password, we have $94^{10}/10^9$ seconds. Dividing by $60$
to get minutes then another $60$ for hours, then $24$ to get days, then $365.25$
to get years, we have $94^{10}/10^9/60/60/24/365.25 = 1706$ years! Again, this
is to try them all, so on average we would find it after looking at half of the
passwords, so it would only take about $850$ years.

:::{note}

A *brute force attack* is one where an attacker tries all possible combinations
of passwords. The number of possible passwords grows exponentially with their
length. As we saw, brute force attacks are most effective against short
passwords.

:::

### Checksums: Detecting Communication Errors

Microcontrollers often need to communicate with other devices, such as sensors,
displays, other microcontrollers, and even the internet. When data is
transmitted between devices, there is always a possibility of errors occurring
during transmission. As a heavy-handed example, imagine a wire is unplugged from
a pin while the data is being transmitted. This doesn't happen often (but
rodents have been known to chew through wires), but other types of errors such
as radio interference, electrical noise, or even cosmic rays can cause data to
become corrupted during transmission. It is important that we have a way to
detect when this happens so that we can take appropriate action, such as
requesting the data to be retransmitted.

A {term}`checksum` is an integer derived from a larger integer and is used to
detect communication errors between devices. There are many different checksum
techniques, but one of the easiest to understand is to add up the digits in a
base-ten integer mod ten and then append that number to the original integer.
Recall that in a computer, everything is represented as bits; music, images, web
pages, Word documents, etc. Sequences of bits are just integers. Rather than
work in the language of bits, binary, 0s and 1s, we will stick with the more
familiar base-ten digits 0–9.

If a microcontroller is transmitting the number $51623$, we would compute the
checksum by computing $(5+1+6+2+3) \bmod 10 = 7$ and we would then transmit the
number `516237`. We call `7` the *checksum digit*, or just *checksum* for short.
What would happen if there was an error in the transmission and the number
transmitted was `596237`? We remove the checksum digit `7` and compute the
checksum of `59623`, which is $(5+9+6+2+3) \bmod 10 = 5$, and we see that $7
\neq 5$, so there must have been an error in the transmission.

Why does this work? This only works if there is a single error in a digit. It is
easy to construct a case where if there were multiple errors, this would not
work. For example, if we were transmitting the value `516237` and there were two
errors in the original communication such as `526137`, the checksum is `7` in
both. If there is only a single error, it makes sense that a change in any
single digit would change the final checksum $\bmod 10$.

:::{exercise}
:label: ex-checksum-check

What is the checksum digit for the integer $198723$?
:::
:::{solution} ex-checksum-check
:class: dropdown

It is $0$ because $(1 + 9 + 8 + 7 + 2 + 3) \bmod 10 = 30 \bmod 10 = 0$.
:::

How can we write a program to compute a checksum? If we have an integer such as
`51623`, we can get the last digit using `% 10`; for example, $51623 \bmod 10 =
3$. Then we need to do the same to the remaining digits `5162`. We can get that
using *integer division* by 10: `51623 // 10 = 5162`. We just keep repeating
this process, adding up the remainder until the number has been reduced to `0`.

We can put this in a function that takes an integer to compute the checksum of
and return the checksum.

```{code-block} python
:linenos:

def checksum(n):                 
    total = 0                    
                             
    while n > 0:                 
        total = total + (n % 10)
        n = n // 10              
    return total % 10            
```

Or more concisely:
* `total += n % 10` instead of `total = total + (n % 10)`
* `n //= 10` instead of `n = n // 10`

:::{exercise}
:label: ex-checksum-review

1. Does the `checksum` function use any local variables?
2. `n` on line 1 is a _______________
3. Line 1 is the function _______________
4. Lines 2–6 constitute the function _______________
5. `total` on line 2 is defined as a _______________ variable.
6. What is the value of `checksum(91242)`?
:::
:::{solution} ex-checksum-review
:class: dropdown

1. Yes, it uses `total` as a local variable to accumulate the sum of digits.
2. `n` on line 1 is a *parameter*
3. Line 1 is the function *definition* (or *header*)
4. Lines 2–6 constitute the function *body*
5. `total` on line 2 is defined as a *local* variable
6. `checksum(91242)` = $(9 + 1 + 2 + 4 + 2) \bmod 10 = 18 \bmod 10 = 8$
:::

How can we append the checksum of an integer to the end (the *least significant
digit*)? For example, if the checksum of $51326$ is $7$, how do we build the new
integer $513267$?

```{code-block} python
:linenos:

# Compute the checksum of x, the integer we want to transmit
check = checksum(x)  
# Multiply x by 10 shifting it left, and then add in the checksum digit 
data = x * 10 + check 
```

(sec-led-fading-brightness)=
### LEDs: Fading Brightness
In @sec-dimming-led, we saw that it is possible to adjust the brightness of an
LED by controlling how long it is on versus off. What if we'd like to gradually
change the brightness of an LED, creating a fading effect? We can achieve this
by using a loop to adjust the on and off times in a way that creates the
illusion of the LED fading in and out.

Let's construct a program that fades an LED from of to full brightness. We can
use a *counting loop* to iterate over the valid PWM levels (i.e., from `0` to
`1023`) and adjust the *duty cycle* accordingly. You will need the circuit from
@sec-wiring-up-led-circuit to follow along.

```{code-block} python
:linenos:
import machine
import time

# create a PWM object for the LED pin
led_pwm = machine.PWM(machine.Pin(32))
# Set frequency to 1 kHz
led_pwm.freq(1000)  

# construct a counting loop
i = 0
while i <= 1023:
    # set the duty cycle to the current value of i
    led_pwm.duty(i)
    # pause for 50ms before the next update
    time.sleep_ms(50)
    # update the counter variable to the next value
    i = i + 1
``` 

:::{exercise}
:label: ex-led-fade-in-time
How long does it take for the LED to fade in from off to full brightness in the program above?
:::
:::{solution} ex-led-fade-in-time
:class: dropdown
The loop iterates from `0` to `1023`, which means it executes `1024` times. Each iteration has a pause of `50ms`, so the total time for the LED to fade in is $1024 \times 50ms = 51200ms$, which is `51.2` seconds.
:::

## Additional Exercises
:::{exercise}
:label: ex-count-1-n
Write a while-loop that prints the integers from 1 to 10, one integer per line. 
:::
:::{solution} ex-count-1-n
:class: dropdown
Here is one solution:
```{code-block} python
i = 1
while i <= 10:
    print(i)
    i = i + 1
```

Does the following program work? If not, fix it.
```{code-block} python
:linenos:
i = 1
while i < 10:
    i = i + 1
    print(i)
```

You could fix it by starting `i` at `0` instead of `1`.
:::

:::{exercise}
:label: ex-countdown
Print the integers counting down from 10 to 0. When you are done print "Blast off!". Add a one-second delay in between integers.
:::
:::{solution} ex-countdown
:class: dropdown
Here is one solution:
```{code-block} python
:linenos:
import time
i = 10
while i >= 0:
    print(i)
    time.sleep(1)  # delay for 1 second
    # update the counter variable to the next value
    i = i - 1
print("Blast off!")
```
:::

:::{exercise}
:label: ex-fibonacci

*The Fibonacci Sequence* is the sequence of integers $0,1,1,2,3,5,8,13\cdots$.
Each Fibonacci number is the sum of the previous two Fibonacci numbers. By
definition the first two Fibonacci numbers are $0$ and $1$. If the first
Fibonacci number is $0$ then the seventh Fibonacci number is $8$. Write a
while-loop to compute the one-hundredth Fibonacci number. 

**Hint:** This is a little tricky. Use two variables, one to keep track of the
current Fibonacci number and one for the previous Fibonacci number. 

:::
:::{solution} ex-fibonacci
The answer you get should be `218922995834555169026`.  This is a surprisingly large number. The Fibonacci sequence actually exhibits exponential growth. 
:::

:::{exercise}
:label: ex-sum-of-squares
Write a while loop to compute the sum of squares from $1$ to $100$, or $1^2 + 2^2 + 3^2 + \cdots + 100^2$.
:::

:::{exercise}
:label: ex-hello-count

How many times will `hello` be printed by the code below?

```{code-block} python
:linenos:
i = 2
while i < 11:
    print("hello")
	i = i + 2
```
:::


:::{exercise}
:label: ex-hello-count-2

How many times will `hello` be printed by the code below?

```{code-block} python
:linenos:
i = 12
while i < 18:
    print("hello")
    i = i + 1
```
:::

:::{exercise}
:label: ex-loop-output

What is the output the code below?

```{code-block} python
:linenos:
i = 1
n = 10
while i < n:
    i = i * 2
print(i)
```
:::

:::{exercise}
:label: ex-num-digits

Write a function `num_digits` that will return the number of digits in an
integer. For example, if we were to call `num_digits(5132981)` it would return
`7` because there are seven digits in `5132981`. Hint: this is similar to the
`checksum` program. 
:::

:::{exercise}
:label: ex-asterisk-triangle

The `*` operator can be applied to a string and an integer. For example, `'Z' *
5` evaluates to `ZZZZZ`. Write a Python program that reads an integer from the
user and prints a triangle pattern of asterisks. For example, if the user enters
`6` then there are six rows of asterisks where the first row has one asterisk
and the sixth row has six asterisks as in the sample output below.

```
Enter n: 6
*
**
***
****
*****
******
```
:::
:::{solution} ex-asterisk-triangle
:class: dropdown
Here is one solution:
```{code-block} python
:linenos:
n = int(input("Enter n: "))

i = 1
while i <= n:
    print('*' * i) 
    i = i + 1
```
:::

:::{exercise}
:label: ex-led-fade-in-out

Write a program that fades an LED in and out continuously. One cycle of fading
in and out should take about 1 second. You can use the code from
@sec-led-fading-brightness as a starting point.
:::