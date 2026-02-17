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