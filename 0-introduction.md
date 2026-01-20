# Introduction
In today's world {term}`computers <computer>` are found almost everywhere we
turn. {term}`Computer Science` is the study of these computers, their design,
and associated computational phenomena.

:::{tip}

You can hover your mouse over terms that are highlighted to see their
definitions. On a mobile device, tap on the highlighted term to see the
definition.

:::

Historically, a computer was an occupation—a person with significant training
and skill in performing mathematical computation. However, engineers have
continually attempted to automate computational tasks, first with mechanical
machines and then, beginning in the early 1900s, electronic devices. By the
midpoint of the century, computers were beginning to take over computational
tasks. This did not replace the human computer, but instead gave rise to a new
occupation: programmer.

## Software is Taking Over
Think about each of the following, what has changed, and if there is software
behind that change:

- How often do you go into a bank and interact with a teller? What do you use
  instead?
- What has happened to book stores, from your local book store to large chain
  stores such as Barnes and Noble and Borders?
- When was the last time you used a travel agent to purchase an airline ticket?
- What has happened to DVD stores such as Blockbuster? What has taken its place?
- What is disrupting the hotel and taxi industry?
- What has happened to music stores where we used to purchase albums and CDs?
- When was the last time you took a roll of film to get developed?
- When was the last time you wrote a letter and mailed it using the post office?
- Your smart phone is a powerful computing device, how often do you look at in a
  day, and what do you use it for?
- Thinking a little further in to the future what could happen to the millions
  of people who drive a vehicle for a living, from taxi drivers to truck
  drivers?

## Electronic Circuits vs Computers
An electronic computer is a special type of electronic {term}`circuit`. Circuits
combine electronic components to perform some predetermined task. Traditionally,
a different circuit is needed for separate tasks. A computer, on the other hand,
avoids this by being a general-purpose circuit designed to execute a sequence of
instructions. If the set of support instructions is general enough, a computer
can perform quite a wide variety of tasks by re-ordering the sequence of
instructions without needing to rewire any of the components.

## Computers vs Microcontrollers
Computers come in all shapes and sizes. We are most familiar with *personal*
computers, which take the form of laptop, desktop, and all-in-one computers.
Smartphones and tablets are also very common. However, a majority of computers
are actually much smaller and are often embedded in other devices. Such
{term}`embedded systems <embedded system>` combine all of the parts of a
computer (e.g., processor, memory, storage, etc.) into a single chip so that it
is easy to integrate into a larger product. These chips often go by the name of
{term}`microcontrollers <microcontroller>`.

```{figure} ./img/fig-microcontrollers.jpg
:label: fig-microcontrollers
:alt: A collection of different microcontroller development boards
:align: left

A collection of different microcontroller development boards. Image by
[Kleinesfilmröllchen](https://commons.wikimedia.org/wiki/File:Microcontroller_collection.jpg), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0), via Wikimedia Commons

```

Microcontrollers typically have significantly less memory and processing power
than a personal computer. They don't run a full {term}`operating system`, but
instead run a single program that is designed to perform a specific task.
Because of their size, computational power, and simplicity, they are often
low-cost and use little power, making them ideal for battery-powered devices.
@fig-microcontrollers shows a collection of different microcontroller chips
on development boards. Common microcontrollers include Atmel's AVR series (used
in Arduino boards), Microchip's PIC series, ESP32 series from Espressif, and
Raspberry Pi Piocs.

Microcontrollers also need to interface with the outside world through sensors
(e.g., temperators sensors, buttons, light sensors, accelorometers, etc.) and
actuators (e.g., motors, lights, displays, speakers, etc.). To do this, they
have external pins that can be connected to other electronic components to read
data from sensors or control actuators. Because the pins can be configured for
various functionality, this is often referred to as 
{term}`general-purpose input/output (GPIO)`. There are many different types of communication protocols
that microcontrollers can use to communicate with sensors and actuators using
these pins that vary in complexity from simple digital on/off signals to complex
serial communication protocols.



@tab-computer-vs-microcontroller summarizes some of the key differences between
computers and microcontrollers. 

:::{table} Comparison of Computers and Microcontrollers
:label: tab-computer-vs-microcontroller
:align: center

| Computers                 | Both                | Microcontrollers                    |
| ------------------------- | ------------------- | ----------------------------------- |
| Discrete components       | Manipulate data     | System on chip (SoC)                |
| Runs an operating system  | Can be reprogrammed | Runs one program every time         |
| Multiple programs running |                     | Minimal resources                   |
| Lots of resources         |                     | Specific Purpose                    |
| General Purpose           |                     | Often control sensors and actuators |
|                           |                     | Pins to connect to circuitry        |

:::