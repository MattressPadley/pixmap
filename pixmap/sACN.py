import sacn
import time


class sACN():
    def __init__(self, num_pixels, pix_channels=3):
        self.sender = sacn.sACNsender()
        self.sender.start()
        self.pix_channels = pix_channels
        self.pix_per_universe = 512 // pix_channels
        self.num_universes = (num_pixels + self.pix_per_universe - 1) // self.pix_per_universe

        for uni in range(self.num_universes):
            self.sender.activate_output(uni + 1)
            output = self.sender[uni + 1]
            if output is not None:
                output.destination = "10.1.4.190"
        
        self.dmx_data = []

        for _ in range(self.num_universes):
            self.dmx_data.append([0] * 512)

        for uni in range(self.num_universes):
            self.sender[uni + 1].dmx_data = self.dmx_data[uni]

    def highlight_pixel(self, pixel):

        # Calculate the universe and channel for the current pixel
        universe = (pixel // self.pix_per_universe) + 1
        channel = (pixel % self.pix_per_universe) * self.pix_channels

        # Set the RGB values for the current pixel
        self.dmx_data[universe - 1][channel] = 255
        self.dmx_data[universe - 1][channel + 1] = 255
        self.dmx_data[universe - 1][channel + 2] = 255
        self.send()

    def clear_pixels(self,):
        for i in range(self.num_universes):
            for j in range(512):
                self.dmx_data[i][j] = 0
        self.send()

    def send(self):
        for i in range(self.num_universes):
            self.sender[i + 1].dmx_data = self.dmx_data[i]

    def stop(self):
        self.sender.stop()
        self.sender = None