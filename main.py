# demo.py
# Kevin McAleer
# test the nRF24L01 modules to send and receive data
# Watch this video for more information about that library https://www.youtube.com/watch?v=aP8rSN-1eT0

from nrf24l01 import NRF24L01
from machine import SPI, Pin
from time import sleep
import struct

csn = Pin(14, mode=Pin.OUT, value=1) # Chip Select Not
ce = Pin(17, mode=Pin.OUT, value=0)  # Chip Enable
led = Pin(25, Pin.OUT)               # Onboard LED

# Define the channel or 'pipes' the radios use.
# switch round the pipes depending if this is a sender or receiver pico

role = "send"
# role = "receive"

if role == "send":
    send_pipe = b"\xe1\xf0\xf0\xf0\xf0"
    receive_pipe = b"\xd2\xf0\xf0\xf0\xf0"
else:
    send_pipe = b"\xd2\xf0\xf0\xf0\xf0"
    receive_pipe = b"\xe1\xf0\xf0\xf0\xf0"

def setup():
    print("Initialising the nRF24L0+ Module")
    nrf = NRF24L01(SPI(0), csn, ce, payload_size=8)
    nrf.open_tx_pipe(send_pipe)
    nrf.open_rx_pipe(1, receive_pipe)
    nrf.start_listening()
    return nrf

def flash_led(times:int=None):
    ''' Flashed the built in LED the number of times defined in the times parameter '''
    for _ in range(times):
        led.value(1)
        sleep(0.01)
        led.value(0)
        sleep(0.1)

def auto_ack(nrf):
    nrf.reg_write(0x01, 0b11111000)

def send(nrf, msg):
    nrf.stop_listening()
    for n in range(len(msg)):
        try:
            print("sending...")
            nrf.send(struct.pack("s",msg[n]))
        except OSError:
            print("Sorry message not sent")
    nrf.start_listening()

def receive(nrf):
    msg = ""
    if nrf.any():
        print("processing message")
        package = nrf.recv()
        message = struct.unpack("s",package)
        msg = message
        print("message received:", str(message))
        flash_led(3)
    return msg

# main code loop

flash_led(1)
nrf = setup()
auto_ack(nrf)
while True:
    send(nrf, "hello world")
    receive(nrf)
    flash_led(1)
    sleep(0.1)
