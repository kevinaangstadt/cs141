'''
    mpy driver for a simple switch with debounce

    Author: Kevin Angstadt Date: 2026-02-15

    BSD-3-Clause License

    Copyright (c) 2026 Kevin Angstadt

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its
       contributors may be used to endorse or promote products derived from this
       software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
    LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
'''

import machine
import time

class Switch:
    '''
    Create a switch object that can be used to detect button presses with debounce.
    :param pin_num: the GPIO pin number where the switch is connected
    :param callback: the function to call when the switch is pressed
    :param trigger: the type of interrupt trigger (default is rising edge)
    :param debounce_ms: the debounce time in milliseconds (default is 200ms)
    '''
    def __init__(self, pin_num, callback, trigger=machine.Pin.IRQ_RISING, debounce_ms=200):
        self.pin = machine.Pin(pin_num, machine.Pin.IN)
        self.callback = callback
        self.debounce_ms = debounce_ms
        self.last_trigger = 0
        
        # Internal handler that checks timing before running the callback
        self.pin.irq(handler=self._internal_handler, trigger=trigger)

    def _internal_handler(self, pin):
        current_time = time.ticks_ms()
        # Check if enough time has passed since the last valid press
        if time.ticks_diff(current_time, self.last_trigger) > self.debounce_ms:
            self.last_trigger = current_time
            # Execute the user-provided function
            self.callback(pin)

    '''
    Get the current value of the switch (0 or 1).
    '''
    def value(self):
        return self.pin.value()