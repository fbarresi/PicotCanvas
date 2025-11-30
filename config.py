import machine
import time

# -------------------------------------------------------------------------
# 1) Display resolution for 7.5" e-paper (800 x 480)
# -------------------------------------------------------------------------
EPD_WIDTH  = 800
EPD_HEIGHT = 480

# -------------------------------------------------------------------------
# 2) Configure the Pico pins and SPI0
# -------------------------------------------------------------------------
#   GP6  = SCK
#   GP7  = MOSI
#   GP4  = MISO (not used but must assign a pin)
#   GP5  = CS
#   GP8  = DC
#   GP9  = RST
#   GP10 = BUSY
spi = machine.SPI(
    0,
    baudrate=2_000_000,
    polarity=0,
    phase=0,
    sck=machine.Pin(6),
    mosi=machine.Pin(7),
    miso=machine.Pin(4)
)

cs_pin   = machine.Pin(5,  machine.Pin.OUT, value=1)
dc_pin   = machine.Pin(8,  machine.Pin.OUT, value=0)
rst_pin  = machine.Pin(9,  machine.Pin.OUT, value=1)
busy_pin = machine.Pin(10, machine.Pin.IN)

def delay_ms(ms):
    time.sleep_ms(ms)

def digital_write(pin, val):
    pin.value(val)

def digital_read(pin):
    return pin.value()

def spi_writebyte(data_block):
    spi.write(data_block)
