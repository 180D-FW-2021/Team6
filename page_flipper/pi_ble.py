# https://pypi.org/project/pygatt/

import pygatt
from binascii import hexlify

adapter = pygatt.GATTToolBackend()

def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    print("Received data: %s" % hexlify(value))

try:
    adapter.start()
    device = adapter.connect('91:2a:70:0e:41:e3')
    device.subscribe("2a19",callback=handle_data)

finally:
    adapter.stop()
