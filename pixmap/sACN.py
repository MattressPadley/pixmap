import sacn
import time


class sACN():
    def __init__(self, num_pixels, pix_channels=3):
        self.sender = sacn.sACNsender()
        self.sender.start()
        self.pix_channels = pix_channels

        num_universes = (num_pixels * pix_channels) // 512

        for i in range(num_universes):
            self.sender.activate_output(i)
            output = self.sender[i]
            if output is not None:
                output.destination = "10.1.2.2"
        
        self.dmx_data = []

        for _ in range(num_universes):
            self.dmx_data.append([0] * 512)

        for uni in range(num_universes):
            self.sender[uni].dmx_data = self.dmx_data[uni]

    def highlight_pixel(self, pixel):
            for i in range(self.pix_channels):
                self.dmx_data[pixel][i] = 255