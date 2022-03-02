import pygatt

# The BGAPI backend will attempt to auto-discover the serial device name of the
# attached BGAPI-compatible USB adapter.
adapter = pygatt.BGAPIBackend()

try:
    adapter.start()
    device = adapter.connect('180F')
    value = device.char_read("2A19")
finally:
    adapter.stop()
