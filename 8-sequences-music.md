# Sequences of Data, Music and Repetition
Music is fundamental to the human experience, and the study of music as a
mathematic science dates back to at least the ancient Greeks. In this chapter,
we will explore how music can be represented as sequences of data, and how we
can use Python to manipulate and generate music.

## Making Sounds with a Buzzer
A buzzer is a simple electronic device that can produce sound when an electric
current is applied to it. There are two types of buzzers: *active* buzzers,
which produce a sound when powered, and *passive* buzzers, which require an
oscillating signal to produce sound. In this section, we will focus on passive
buzzers, as they allow us to create different tones by varying the frequency of
the signal.

:::{exercise}
:label: ex-oscillating-signal-check
How can we generate an oscillating signal using MicroPython?
:::
:::{solution} ex-oscillating-signal-check
We can create a `PWM` object on a pin connected to the buzzer and set its frequency and duty cycle to produce sound. 
:::

### Wiring a Buzzer
A buzzer is very simple to connect to a microcontroller. If you have both an active and a passive buzzer, make sure you are using the passive one for this chapter. The passive buzzer will typically have an exposed circuit board on the bottom with two pins while an active buzzer will have epoxy covering the bottom where the pins are.

Components you will need:
- Breadboard
- Passive buzzer
- Jumper wires

@fig-buzzer shows a passive buzzer connected directly to the ESP32 on GPIO pin
32. If your buzzer has long leads, you can make this direct connection. If your
buzzer has short pins, place them in the breadboard and use jumper wires to
connect them to the ESP32. The positive pin of the buzzer should be connected to
a GPIO pin on the ESP32, and the negative pin should be connected to a ground
(GND) pin. The positive pin is usually marked with a "+" symbol, a longer lead,
or red coloring.

```{figure} img/fig-buzzer.png
:align: center
:alt: A passive buzzer connected to a breadboard with jumper wires.
:label: fig-buzzer
A passive buzzer connected to a breadboard with jumper wires.
```

### Generating Tones
To generate a tone with a passive buzzer, we need to create an oscillating
signal. This can be done using the `PWM` class from the `machine` module in
MicroPython. We want a nice square wave, so we will set the duty cycle to 50%,
which means the signal will be high for half of the time and low for the other
half. Then, we can vary the frequency of the signal to produce different tones. 

The frequency of a sound wave determines its pitch, with higher frequencies
producing higher-pitched sounds and lower frequencies producing lower-pitched
sounds. A common reference point for musical notes is the A4 note, which has a
frequency of 440 Hz. 

Let's make our buzzer play the A4 note:

```{code-block} python
:linenos:
import machine

buzzer = machine.PWM(machine.Pin(32))
buzzer.freq(440)  # Set frequency to 440 Hz (A4 note)
buzzer.duty(511)  # Set duty cycle to 50% (511 out of 1023)
```

Does the noise grate on your nerves a bit? We need to come up with a sequence
of tones that sounds more like music and less like a car alarm.

## Musical Notes
In Western music, there are 12 distinct notes in an octave: C, C#, D, D#, E, F,
F#, G, G#, A, A#, and B. The `#` symbol is read as *sharp* and denotes a
semitone higher than the natural note. Each octave is successively higher in
pitch than the previous one. While we could calculate the frequency of each note
using the formula for equal temperament tuning, it is often more convenient to
use a predefined mapping of note names to frequencies.

To save you the hassle, we have precomputed the frequencies for the eight and a bit octaves for you. Create a file called `note.py`and add the following code to it:

```{code-block} python
:linenos:
# notes
REST = 0

# Octave 0
C0 = 16
CS0 = 17
D0 = 18
DS0 = 19
E0 = 21
F0 = 22
FS0 = 23
G0 = 25
GS0 = 26
A0 = 28
AS0 = 29
B0 = 31

# Octave 1
C1 = 33
CS1 = 35
D1 = 37
DS1 = 39
E1 = 41
F1 = 44
FS1 = 46
G1 = 49
GS1 = 52
A1 = 55
AS1 = 58
B1 = 62

# Octave 2
C2 = 65
CS2 = 69
D2 = 73
DS2 = 78
E2 = 82
F2 = 87
FS2 = 93
G2 = 98
GS2 = 104
A2 = 110
AS2 = 117
B2 = 123

# Octave 3
C3 = 131
CS3 = 139
D3 = 147
DS3 = 156
E3 = 165
F3 = 175
FS3 = 185
G3 = 196
GS3 = 208
A3 = 220
AS3 = 233
B3 = 247

# Octave 4 (Middle C is C4)
C4 = 262
CS4 = 277
D4 = 294
DS4 = 311
E4 = 330
F4 = 349
FS4 = 370
G4 = 392
GS4 = 415
A4 = 440
AS4 = 466
B4 = 494

# Octave 5
C5 = 523
CS5 = 554
D5 = 587
DS5 = 622
E5 = 659
F5 = 698
FS5 = 740
G5 = 784
GS5 = 831
A5 = 880
AS5 = 932
B5 = 988

# Octave 6
C6 = 1047
CS6 = 1109
D6 = 1175
DS6 = 1245
E6 = 1319
F6 = 1397
FS6 = 1480
G6 = 1568
GS6 = 1661
A6 = 1760
AS6 = 1865
B6 = 1976

# Octave 7
C7 = 2093
CS7 = 2217
D7 = 2349
DS7 = 2489
E7 = 2637
F7 = 2794
FS7 = 2960
G7 = 3136
GS7 = 3322
A7 = 3520
AS7 = 3729
B7 = 3951

# Octave 8
C8 = 4186
CS8 = 4435
D8 = 4699
DS8 = 4978
```

Notice that we can't use `#` in a variable name for sharps, so we use `S`
instead. We also have a special note called `REST` which has a frequency of 0.
This is used to represent a pause in the music where no sound is played. Upload this file to your microcontroller so that we can `import`it in our main program.

This handles the *pitch* of the notes, but we also need to specify the
*duration* of each note. In music, the duration of a note is often represented
as a fraction of a whole note. For example, a quarter note is 1/4 of a whole
note, an eighth note is 1/8 of a whole note, and so on. We can represent these
durations as constants in our program as well.

Create a file called `music.py`, and we will get started writing some code to play music with our buzzer in the next section.

```{code-block} python
:linenos:

import machine
import time

import note

# define the tempo (beats per minute)
# in many musical pieces, this is the number of quarter notes that 
# can be played in one minute.
tempo = 120

# calculate note durations (ms) based on this tempo
quarter = 60000 // tempo

# calculate the duration of other note types based on the quarter note
whole = quarter * 4
half = quarter * 2
eighth = quarter // 2
sixteenth = quarter // 4

# dotted notes (standard note + half its value)
dotted_hole = int(whole * 1.5)
dotted_half = int(half * 1.5)
dotted_quarter = int(quarter * 1.5)
dotted_eighth = int(eighth * 1.5)

# triplet notes (standard note * 2/3)
quarter_triplet = int(half // 3)
eighth_triplet = int(quarter // 3)

# create a PWM object for the buzzer
buzzer = machine.PWM(machine.Pin(32))
```

It would be rather laborious, but we could now write out a program that plays a
song by setting the frequency of our PWM object to the appropriate note
frequencies and using `time.sleep_ms()` to wait for the duration of each note.
However, it would be much more convenient to represent a song as a sequence of
notes and durations, and then *iterate* through that sequence to play the music.
We will explore how to do this in the next section.

## Tuples
A {term}`tuple` is an ordered pair (or triple, or quadruple, etc.). A tuple in
MicroPython combines two or more values into a single value using parentheses
with the component values separated by commas. For example, the tuple
`(200,300)` represents a single value with two integer components.

A tuple need not contain integers. Any time we want to think of several values as a single value we can use a tuple. For example, we can use a tuple to hold a name such as `("Dorothy", "Vaughan")` which might be more helpful than storing the name as a single string `"Dorothy Vaughan"`.[^dorothy]

[^dorothy]: [Dorothy Vaughan](https://en.wikipedia.org/wiki/Dorothy_Vaughan) was an African American mathematician and computer programmer who worked at NASA during the Space Race. She was one of the first African American women to be promoted to a supervisory position at NASA and made significant contributions to the success of the early space missions.

Each of the elements in a tuple is *indexed* by its position in the tuple, counting from 0. We access the elements of a tuple using the index operator `[]`. For example:

```{code-block} python
:linenos:
name = ("Dorothy", "Vaughan")
print(name[1], name[0])
```

This will print `Vaughan Dorothy` because `name[1]` is the second element of the tuple (the last name) and `name[0]` is the first element of the tuple (the first name).

Tuples have a *length*, which is the number of elements contained within the tuple. We can find the length of a tuple using the built-in `len()` function. For example:

```{code-block} python
:linenos:
name = ("Dorothy", "Vaughan")
print(len(name))
```
This will print `2` because there are two elements in the tuple.

It is also possible to *decompose* a tuple into its individual components using an assignment statement. The number of variables on the left-hand side of the assignment must match the number of elements in the tuple. For example:

```{code-block} python
:linenos:
name = ("Dorothy", "Vaughan")
(first_name, last_name) = name
print(first_name)
print(last_name)
```
This will print `Dorothy` and `Vaughan` on separate lines because the tuple `name` is decomposed into the variables `first_name` and `last_name`.

It is important to note that tuples are {term}`immutable`, which means that once a tuple is created, its elements cannot be changed. If we want to create a new tuple with different values, we must create a new tuple rather than modifying the existing one. If we tried to change a component of a tuple, we would get an error. For example:

```{code-block} python
:linenos:
name = ("Dorothy", "Vaughan")
name[0] = "Mary"
```
This will raise a `TypeError` because we cannot modify the elements of a tuple.

Tuples are extremely helpful for structuring data where we wish to group related
values together. In our music programs, we will use tuples to represent notes
and their durations as pairs of values. For example, we might represent a note
as a tuple like `(quarter, note.C4)` which indicates that we want to play the C4
note for the duration of a quarter note.

## Lists

A list in Python is a lot like a tuple, except that it is {term}`mutable`. This
means that we can change the elements of a list after it has been created.  We define a list using square brackets `[]` instead of parentheses. For example, we could define a list of musical notes like this:

```{code-block} python
:linenos:
import note

# define a song as a list of (duration, note) tuples
song = [
    (eighth, note.G4), 
    (eighth, note.G4), 
    (eighth, note.G4), 
    (half, note.DS4), 
    
    (quarter, note.REST),
    
    (eighth, note.F4), 
    (eighth, note.F4), 
    (eighth, note.F4), 
    (half, note.D4),
    
    (whole, note.REST)
]
```

:::{note}
A list can be defined on a single line. In the example above, we define it over
 multiple lines for readability, but we could have also written it as:

```{code-block} python
:linenos:
song = [(eighth, note.G4), (eighth, note.G4), (eighth, note.G4), (half, note.DS4), (quarter, note.REST), (eighth, note.F4), (eighth, note.F4), (eighth, note.F4), (half, note.D4), (whole, note.REST)]
```
:::

All of the operations that work on a tuple also work on a list, but since a list is mutable, we can also modify it after it has been created. For example, we can use the index operator to change an element of the list:

```{code-block} python
:linenos:
song[0] = (quarter, note.G4)  # Change the first note to a quarter note
```

We can also use the `append()` method to add a new element to the end of the list:

```{code-block} python
:linenos:
song.append((half, note.C5))  # Add a new note to the end of the song
```
This will add the note C5 with a duration of a half note to the end of the `song` list.

:::{exercise}
:label: ex-list-looping
How can we use `len()` and index access to loop through the elements of a list?
:::
:::{solution} ex-list-looping

This is just our common counting loop structure from before. We start our
counting at 0 and need to continue while we are less than the length of the
list. (Because the first index is 0, we can never actually have an index equal
to the length of the list, so we use `<` rather than `<=` in our loop
condition.)

To play our song, we can loop through the `song` list and for each element, we
can extract the duration and note from the tuple, set the frequency of the
buzzer to the note, and then sleep for the duration of the note. Here is how we
can do this:

```{code-block} python
:linenos:

i = 0
while i < len(song):
    # Get the duration and pitch from the current element
    duration, pitch = song[i]

    # if the pitch is a rest, we need to turn off the buzzer
    if pitch == note.REST:
        buzzer.duty(0)  # Turn off the buzzer
    else:
        buzzer.freq(pitch)  # Set the frequency to the pitch
        buzzer.duty(511)  # Turn on the buzzer with 50%
    
    # Wait for the duration of the note
    # We will sleep for all but 10 ms of the note duration to create 
    # a slight separation between notes
    time.sleep_ms(duration - 10)
    buzzer.duty(0)  # Turn off the buzzer to create a separation
    time.sleep_ms(10)  # Wait for 10 ms before playing the next note

    # increase our counter to move to the next element in the list
    i += 1 
```
:::

## Making Music
Now, it's your turn to make some music! You can create your own song by defining
a list of (duration, note) tuples. You can use the `note` module to access the
frequencies of the notes and the duration constants defined in `music.py` to
specify the durations. Try creating a simple melody or even a full song!

For example, here is another classic melody:

```{code-block} python
:linenos:
song = [
    (quarter, note.G4), (eighth, note.REST), 
    (eighth, note.D4), (quarter, note.G4), (eighth, note.REST), 
    (eighth, note.D4),
    
    (eighth, note.G4), (eighth, note.D4), (eighth, note.G4), (eighth, note.B4),
    (quarter, note.D5), (quarter, note.REST),
    
    (quarter, note.C5), (eighth, note.REST),
    (eighth, note.A4), (quarter, note.C5), (eighth, note.REST),
    (eighth, note.A4),
    
    (eighth, note.C5), (eighth, note.A4), (eighth, note.FS4), (eighth, note.A4),
    (quarter, note.D4), (quarter, note.REST)
]
```

Do you recognize it?

## The `for` Loop
Looking back at @ex-list-looping, there were a number of pieces we had to get
correct to loop through the list of notes. We had to initialize our counter
variable `i` to 0, we had to make sure our loop condition was correct, and we
had to remember to increment `i` at the end of each iteration. This is a lot of
details to keep track of, and it is easy to make a mistake that causes an
infinite loop or an *off-by-one error*.

Fortunately, Python provides a more convenient way to loop through the elements of a sequence type such as a list or tuple. This is called a `for` loop, and it allows us to iterate directly over the elements of the sequence without having to manage a counter variable. 

A `for` loop has the following syntax:

```{code-block} python
:linenos:
for variable in some_sequence_data:
    statements
```

In the code block above, `some_sequence_data` is a value that is a sequence type
(such as a list or tuple). There are two new MicroPython keywords `for` and
`in`. The `for` loop will iterate through each element of `some_sequence_data`,
and for each element, it will assign that element to the variable `variable` and
then execute the block of statements indented under the `for` loop. `variable`
should be thought of as a temporary variable that takes on the value of each
element in the sequence as we iterate through it, and it really should only be
accessed in the body of the `for` loop.

Notice that we don't have to explicitly keep track of our position in the
sequence with a counter variable, and we don't have to worry about the loop
condition or incrementing a counter. The `for` loop takes care of all of that
for us, which makes our code cleaner and less error-prone.

We can use a `for` loop to iterate through our `song` list and play the music without having to manage a counter variable. Here is how we can do this:

```{code-block} python
:linenos:
for note_info in song:
    # decompose the note_info tuple into duration and pitch
    # NOTE: you can technically decompose the tuple directly in loop header
    (duration, pitch) = note_info

    if pitch == note.REST:
        # Turn off the buzzer
        buzzer.duty(0)  
    else:
        # Set the frequency to the pitch
        buzzer.freq(pitch)  
        # Turn on the buzzer with 50% duty cycle
        buzzer.duty(511)  
    
    time.sleep_ms(duration - 10)
    # Turn off the buzzer to create a separation
    buzzer.duty(0)  
    # Wait for 10 ms before playing the next note
    time.sleep_ms(10)  
```

### Revisiting the Counting Loop
Recall that a very common looping pattern is a *counting loop* that iterates an
exact number of times. Recall the pattern ...

```{code-block} python
:linenos:
i = 0
while i < n:
    # loop body
	i = i + 1
```

This loop body will execute exactly `n` times; as long as `n` is not modified in
the loop body. This can be rewritten using a `for` loop and the built-in
`range()` function as follows:

```{code-block} python
:linenos:
for i in range(n):
    # loop body
```

Observe that there is also no explicit assignment statement incrementing `i` by one. The `range(n)` function generates a sequence of integers starting from 0 up to (but not including) `n`, and the `for` loop iterates through this sequence, assigning each value to `i` in turn.

```{note}
The `range()` function does not produce a list or tuple of integers. Instead, it
 produces a *range type*, which is used to generate an immutable sequence of 
 integers. This is more efficient because it creates the numbers "on the fly" as
 needed rather than storing them all in memory at once. Since it is still a 
 sequence type, we can use it with a `for` loop to iterate through the generated
 integers.
```

The `for`-loop below will print the integers 0 through 9, one per line.

```{code-block} python
:linenos:
for i in range(10):
    print(i)
```

### `for` Loop Examples
Here is an example `for` loop that will add up the integers from 1 to 100.

```{code-block} python
:linenos:
total = 0
for i in range(101):
    total = total + i
```

#### Variations on `range()`
The `range` function can take an optional starting value. For example
`range(10,15)` generates the sequence of integers `10, 11, 12, 13, 14` (it never
includes the *stop* value, in this case `15`).

:::{exercise}
:label: ex-range-looping
What is the output of the following code?
```{code-block} python
:linenos:
sum = 0
for i in range(3,8):
    sum += i
print(sum)
```
:::
:::{solution} ex-range-looping
The output of the code will be `25`. Because `3+4+5+6+7` is `25`.
:::

:::{exercise}
:label: ex-range-looping-semi-reversed
What is the output of the following code?
```{code-block} python
:linenos:
sum = 0
for i in range(8,3):
    sum += i
print(sum)
```
:::
:::{solution} ex-range-looping-semi-reversed
```
0
```
Because the start value in the `range` function is greater-than-or-equal to the
 stop value, the loop iterates exactly zero times.
:::

The `range` function can also take an optional *step* value as the third argument. For example, `range(10,15,2)` generates the sequence of integers `10, 12, 14`.

:::{exercise}
:label: ex-range-looping-step
What is the output of the following code?
```{code-block} python
:linenos:
sum = 0
for i in range(3,8,2):
    sum += i
print(sum)
```
:::
:::{solution} ex-range-looping-step
The output of the code will be `15`. Because `3+5+7` is `15`.
:::

Step values can be negative. For example, `range(8,3,-1)` generates the sequence
`8,7,6,5,4` (why does it not include `3`? Because the `range` function never
includes the final *stop* value, in this case `3`).

#### Calculating Averages and Medians
`for` loops are very convenient for solving problems that involve iterating
through a sequence of data. Let's say you have a list of grades and would like
to calculate both the average grade and the median (middle) grade. We can do this with a `for` loop as follows:

```{code-block} python
:linenos:
grades = [85, 92, 78, 90, 88]

# Calculate the average
total = 0
for grade in grades:
    total += grade
average = total / len(grades)
```

Calculating the median requires sorting the list of grades and then finding the middle element (or the average of the two middle elements if there is an even number of grades). In MicroPython, list data has a built-in `sort()` method that we can call:

```{code-block} python
:linenos:
:lineno-start: 9
# Sort the list of grades in place
grades.sort()  

# Calculate the median
n = len(grades)
if n % 2 == 1:
    # If there is an odd number of grades, the median is the middle element
    median = grades[n // 2]
else:
    # If there is an even number of grades, the median is the average of the two
    # middle elements
    median = (grades[n // 2 - 1] + grades[n // 2]) / 2
``` 

#### The Birthday Paradox

The *Birthday Paradox* (also called the *Birthday Problem*) is a
counterintuitive result in probability that asks how many people need to be in a
room for there to be a 50% chance that two people share a birthday. As is often
the case, many of our examples seem silly, but have real applications. In the
area of computer security there is a particular type of attack called a [*birthday attack*](https://en.wikipedia.org/wiki/Birthday_attack).  The popular
radio show *This American Life* did an
[episode](https://www.thisamericanlife.org/630/things-i-mean-to-know) titled
[Fraud Complex](https://www.thisamericanlife.org/630/things-i-mean-to-know/act-one-0) where the results from the birthday paradox were used to debunk claims
of voter fraud.[^fraud]

[^fraud]: [_One Person, One Vote: Estimating the Prevalence of Double Voting in U.S. Presidential Elections_](https://5harad.com/papers/1p1v.pdf)

The mathematics for solving the birthday problem, while not all that
complicated, is beyond the scope of this text. However, writing a program to
simulate the birthday problem is fairly straightforward.

There are 366 possible birthdays (including the leap year day February 29). We
can think of the calendar as a list of 366 integers. Call this list `birthdays`.
The number of people in the room that share January 1 as a birthday is in
`birthdays[0]` and the number that share December 31 is in `birthdays[365]`.
Initially `birthdays` is initialized to all zeros.

```{code-block} python
:linenos:
birthdays = []

# Append 366 zeros to the `birthdays` list
for i in range(366):
    birthdays.append(0)
```


Python has an even simpler notation for initializing a list to all of the same
value. The three lines of code above can be replaced with the one line:

```{code-block} python
:linenos:
birthdays = [0]*366
```

How can we simulate someone's birthday?  Generate a random number between 0 and
365 and increment the corresponding birthday in the `birthdays` list.

```{code-block} python
:linenos:
import random

bday = random.randrange(366)
birthdays[bday] += 1
```

We need to do this a number of times, once for each person in the room. How many
times? This is precisely what we are trying to figure out. Let's start with 100. 

```{code-block} python
:linenos:

# Generate one hundred random birthdays
for i in range(100):
    bday = random.randrange(366)
    birthdays[bday] += 1
```

How do we know if two or more people share a birthday? One of the items in the
`birthdays` list will be greater than 1. If nobody shared a birthday then all of
the integers in `birthdays` are either 0 or 1. By the [*pigeonhole principle*](https://en.wikipedia.org/wiki/Pigeonhole_principle) if there are 367
people in the room then we are guaranteed that at least two people share a
birthday. In practice though, it is much less than that.

```{code-block} python
:linenos:
i = 0
for count in birthdays:
    if count > 1:
        print(count, "birthdays on day", i)
    i = i + 1
```

If we run this with 100 people in the room we see that lots of people share a
birthday. (You will get different results because we are generating random
birthdays).

```
2 birthdays on day 10
2 birthdays on day 23
2 birthdays on day 49
2 birthdays on day 69
3 birthdays on day 95
2 birthdays on day 144
2 birthdays on day 178
2 birthdays on day 290
3 birthdays on day 315
2 birthdays on day 316
2 birthdays on day 333
```

In fact with 100 people, you are almost guaranteed to have people share a
birthday. With a little experimenting you can see that at about 23 people there
is a 50% chance of two or more people sharing a birthday. It is called the
*Birthday Paradox* because 23 *seems* like a surprisingly small number.


### Nested `for` Loops

`for` loops can be nested just like `while` loops. This is a pattern we will see
frequently when we deal with two-dimensional data, like tables. Consider the
code fragment below:

```{code-block} python
:linenos:
for i in range(4):
    for j in range(3):
        print(i,'\t',j)
```

For each value of `i` in the *outer* `for` loop `j` will take on values `0`,`1`,
and `2` in the *inner* `for`-loop. The output produced is:

```
0 	 0
0 	 1
0 	 2
1 	 0
1 	 1
1 	 2
2 	 0
2 	 1
2 	 2
3 	 0
3 	 1
3 	 2
```

This one is slightly more tricky, but one you will see again.

:::{exercise}
:label: ex-nested-for-loop
What is the output of the following code?
```{code-block} python
:linenos:
for i in range(4):
    for j in range(i,3):
        print(i,'\t',j)
```
:::
:::{solution} ex-nested-for-loop
The way to think of this is that for each value `i` `j` will take on value from `i` 
up to but not including `3`.
```
0 	 0
0 	 1
0 	 2
1 	 1
1 	 2
2 	 2
```
:::

## Additional Exercises

:::{exercise}
:label: ex-compare-triplets
"Compare The Triplets"[^compare-the-triplets] 

[^compare-the-triplets]: https://www.hackerrank.com/challenges/compare-the-triplets/problem

Suppose Alice creates a programming problem for HackerRank and a reviewer rates
the question based on clarity, originality, and difficulty where each value is
between 1 and 100. For example the tuple `(90, 10, 50)` means the problem is
clear (90), not very original (10), and is of medium difficulty (50).

Suppose Bob also creates a problem for HackerRank with a rating of `(75,50,60)`.
We would like to compare Alice's and Bob's problems awarding a point for each
criteria that is greater than the other's. For example, in this case Alice's
score is `1` because her score on clarity is greater than Bob's.  Bob's score is
`2` because his problem is more original and harder. No point is allotted for
values that are the same.

Complete the function `compareTheTriplets` below. It must return a tuple of two
integers, the first being Alice's score and second being Bob's. The two
paramaters are `a`, a tuple or list of three integers that represent Alice's
rating, and `b`, a tuple or list of three integers that represents Bob's rating.

The input consists of two lines of three space separated integers. The first
line is for Alice, and the second line is for Bob.

*Sample Input 0*
```
5 6 7
3 6 10
```

*Sample Output 0*
```
1 1
```

*Sample Input 1*
```
17 28 30
99 16 8
```

*Sample Output 1*
```
2 1
```

```{code-block} python
:linenos:
def compareTheTriplets(a,b):
    # fill in function body


# M a i n   P r o g r a m

# Don't worry about how the main program works

# Test Sample Input 0
if compareTheTriplets([5,6,7],[3,6,10]) == (1,1):
    print("Sample Input 0 Passed")
else:
    print("Sample Input 0 Failed")

# Test Sample Input 1
if compareTheTriplets((17,28,30),(99,16,8)) == (2,1):
    print("Sample Input 1 Passed")
else:
    print("Sample Input 1 Failed")

# Try your own inputs
a = [int(x) for x in input("Alice:").split()]
b = [int(x) for x in input("Bob:").split()]
print(' '.join([str(x) for x in compareTheTriplets(a,b)]))

```
:::

:::{exercise}
:label: ex-mini-max-sum
"Mini-Max Sum"[^mini-max-sum]

[^mini-max-sum]: https://www.hackerrank.com/challenges/mini-max-sum/problem

Given a list of five integers find the minimum and maximum value that can be
calculated by summing exactly four of the five values. For example, if the list
was `[7,9,3,1,5]` the maximum would be $7 + 9 + 3 + 5 = 24$ and the minimum
would be $7 + 3 + 1 + 5 = 16$.

Complete the `miniMaxSum` function below, where `arr` is a list of five
integers. The function should return a tuple where the first item is the minimum
sum and the second item is the maximum sum.

*Sample Input 0*
```
1 2 3 4 5
```

*Sample Output 0*
```
10 14
```

```{code-block} python
:linenos:
def miniMaxSum(arr):
    # fill in function body


# M a i n   P r o g r a m

# Don't worry about how the main program works

if miniMaxSum([7,9,3,1,5]) == (16,24):
    print("Sample Test 0 Passed")
else:
    print("Sample Test 0 Failed")

# Try your own list of numbers
v = [int(x) for x in input("numbers: ").split()]
print(' '.join([str(x) for x in miniMaxSum(v)]))
```
:::

:::{exercise}
:label: ex-two-sum

Given a value `k` on one line and a list of integers on the second, complete the
function `twoSum` below that returns `true` if two of the integers from `nums`
add up to `k`.

*Sample Input 0*
```
25
4 9 33 2 16
```

*Sample Output 0*
```
True
```

because $9+16=25$.

*Sample Input 1*
```
14
4 9 33 2 16
```

*Sample Output 1*
```
False
```

```{code-block} python
:linenos:
def twoSum(nums, k):
    # fill in function body

# M a i n   P r o g r a m

# Don't worry about how the main program works

# Try your own inputs
print(twoSum([4,9,33,2,16], 25))  # True
print(twoSum([4,9,33,2,16], 14))  # False

# Try your own k and list of integers
k = int(input("k: "))
nums = [int(x) for x in input("Numbers:").split()]
print(twoSum(nums,k))
```
:::

:::{exercise}
:label: ex-product-of-others

This comes from the [Daily Coding Problem](https://www.dailycodingproblem.com/) email list. 

Given a list of integers, return a new list such that each element at index $i$
of the new list is the product of all the numbers in the original list except
the one at index $i$.

For example, if our input was `[1, 2, 3, 4, 5]`, the expected output would be
`[120, 60, 40, 30, 24]`. If our input was `[3, 2, 1]`, the expected output would
be `[2, 3, 6]`.

Follow-up: what if you can't use division?
:::

:::{exercise}
:label: ex-staircase

Conside a staircase of size `n = 4`.[^staircase]

[^staircase]: This exercise is adapted from a problem on HackerRank called
    "Staircase". You can find the original problem
    [here](https://www.hackerrank.com/challenges/staircase/problem).

```
   #
  ##
 ###
####
```

The height and width are equal to `n`. The image is drawn using `#`
symbols and spaces. The last line does not have any spaces in it.

Complete the function `staircase` below. It should print a staircase as defined
above. The input `n` is the size of the staircase (its width and height). Assume
`n` is greater than 0.

*Sample Input 0*
```
n: 6
```

*Sample Output 0*
```
     #
    ##
   ###
  ####
 #####
######
```

```{code-block} python
:linenos:
def staircase(n):
    # fill in function body

# M a i n    P r o g r a m
staircase(int(input('n: ')))
```
:::