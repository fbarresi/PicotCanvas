import config


class EPD:
    def __init__(self):
        self.reset_pin = config.rst_pin
        self.dc_pin = config.dc_pin
        self.busy_pin = config.busy_pin
        self.cs_pin = config.cs_pin
        self.width = config.EPD_WIDTH
        self.height = config.EPD_HEIGHT
        self.BLACK  = 0x000000   #   0000  BGR
        self.WHITE  = 0xffffff   #   0001
        self.YELLOW = 0x00ffff   #   0010
        self.RED    = 0x0000ff   #   0011
        # self.ORANGE = 0x0080ff   #   0100
        self.BLUE   = 0xff0000   #   0101
        self.GREEN  = 0x00ff00   #   0110
        

    # Hardware reset
    def reset(self):
        config.digital_write(self.reset_pin, 1)
        config.delay_ms(20) 
        config.digital_write(self.reset_pin, 0)         # module reset
        config.delay_ms(2)
        config.digital_write(self.reset_pin, 1)
        config.delay_ms(20)   

    def send_command(self, command):
        config.digital_write(self.dc_pin, 0)
        config.digital_write(self.cs_pin, 0)
        config.spi_writebyte(bytes([command]))
        config.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        config.digital_write(self.dc_pin, 1)
        config.digital_write(self.cs_pin, 0)
        config.spi_writebyte(bytes([data]))
        config.digital_write(self.cs_pin, 1)

    def send_data_block(self, data_block):
        config.digital_write(self.dc_pin, 1)
        config.digital_write(self.cs_pin, 0)
        config.spi_writebyte(data_block)
        config.digital_write(self.cs_pin, 1)
        
    # send a lot of data   
    def send_data2(self, data, chunk_size=512):
        idx = 0
        length = len(data)
        while idx < length:
            end = min(idx + chunk_size, length)
            slice_data = data[idx:end]
            self.send_data_block(slice_data)
            idx = end

    def send_zeros_in_chunks(self, total_size, chunk_size=512):
        zero_chunk = b'\x11' * chunk_size
        sent = 0
        while sent < total_size:
            remain = total_size - sent
            if remain >= chunk_size:
                self.send_data_block(zero_chunk)
                sent += chunk_size
            else:
                self.send_data_block(b'\x11' * remain)
                sent += remain
        
    def read_busy(self):
        print("e-Paper busy H")
        while(config.digital_read(self.busy_pin) == 0):      # 0: busy, 1: idle
            config.delay_ms(5)
        print("e-Paper busy H release")

    def turn_on_display(self):
        self.send_command(0x04) # POWER_ON
        self.read_busy()

        self.send_command(0x12) # DISPLAY_REFRESH
        self.send_data(0X00)
        self.read_busy()
        
        self.send_command(0x02) # POWER_OFF
        self.send_data(0X00)
        self.read_busy()
        
    def init(self):
        # EPD hardware init start
        self.reset()
        self.read_busy()
        config.delay_ms(30)

        self.send_command(0xAA)   
        self.send_data(0x49)
        self.send_data(0x55)
        self.send_data(0x20)
        self.send_data(0x08)
        self.send_data(0x09)
        self.send_data(0x18)

        self.send_command(0x01)
        self.send_data(0x3F)

        self.send_command(0x00)  
        self.send_data(0x5F)
        self.send_data(0x69)

        self.send_command(0x03)
        self.send_data(0x00)
        self.send_data(0x54)
        self.send_data(0x00)
        self.send_data(0x44) 

        self.send_command(0x05)
        self.send_data(0x40)
        self.send_data(0x1F)
        self.send_data(0x1F)
        self.send_data(0x2C)

        self.send_command(0x06)
        self.send_data(0x6F)
        self.send_data(0x1F)
        self.send_data(0x17)
        self.send_data(0x49)

        self.send_command(0x08)
        self.send_data(0x6F)
        self.send_data(0x1F)
        self.send_data(0x1F)
        self.send_data(0x22)

        self.send_command(0x30)
        self.send_data(0x03)

        self.send_command(0x50)
        self.send_data(0x3F)

        self.send_command(0x60)
        self.send_data(0x02)
        self.send_data(0x00)

        self.send_command(0x61)
        self.send_data(0x03)
        self.send_data(0x20)
        self.send_data(0x01) 
        self.send_data(0xE0)

        self.send_command(0x84)
        self.send_data(0x01)

        self.send_command(0xE3)
        self.send_data(0x2F)

        self.send_command(0x04)
        self.read_busy()
        return 0

    def display(self, image):
        self.send_command(0x10)
        self.send_data2(image)

        self.turn_on_display()
        
    def clear(self, color=0x11):
        self.send_command(0x10)
        #self.send_data2([color] * int(self.height) * int(self.width/2))
        size = (self.width * self.height)
        self.send_zeros_in_chunks(size)

        self.turn_on_display()
        
    def display_image(self, path="images/image.bin"):
        with open(path, "rb") as f:
            image_data = f.read()
        self.display(image_data)

    def sleep(self):
        self.send_command(0x07) # DEEP_SLEEP
        self.send_data(0XA5)
        
        config.delay_ms(2000)


def main():
    epd = EPD()
    epd.init()

    # Clear the screen
    epd.clear()

    # Suppose you uploaded an 800x480 BIN file to the Pico (flash),
    # containing 48,000 bytes of 1-bit data:
    with open("images/image.bin", "rb") as f:
        image_data = f.read()

    # Display it
    epd.display(image_data)

    # Wait a few seconds, then sleep
    config.delay_ms(5000)
    epd.sleep()

if __name__ == "__main__":
    main()