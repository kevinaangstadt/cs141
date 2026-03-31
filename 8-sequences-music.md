# Sequences of Data and Music
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
:label: oscillating-signal-check
How can we generate an oscillating signal using MicroPython?
:::
:::{solution} oscillating-signal-check
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
:label: list-looping
How can we use `len()` and index access to loop through the elements of a list?
:::
:::{solution} list-looping

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
    # Get the duration and note from the current element
    duration, note = song[i]

    # if the note is a rest, we need to turn off the buzzer
    if note == note.REST:
        buzzer.duty(0)  # Turn off the buzzer
    else:
        buzzer.freq(note)  # Set the frequency to the note
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