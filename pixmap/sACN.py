import sacn
import json


class sACN():
    """
    This class represents the sACN (Streaming ACN) protocol for controlling pixel-based lighting fixtures.

    Args:
        num_pixels (int): The total number of pixels to control.
        pix_channels (int, optional): The number of channels per pixel. Defaults to 3.

    Attributes:
        sender (sacn.sACNsender): The sACN sender object.
        pix_channels (int): The number of channels per pixel.
        pix_per_universe (int): The number of pixels per universe.
        num_universes (int): The total number of universes required to control all the pixels.
        dmx_data (list): A list of DMX data for each universe.

    Methods:
        highlight_pixel(pixel): Highlights a specific pixel by setting its RGB values to maximum.
        clear_pixels(): Clears all the pixels by setting their RGB values to zero.
        send(): Sends the DMX data to the lighting fixtures.
        stop(): Stops the sACN sender.

    """

    def __init__(self):
        self.sender = sacn.sACNsender('0.0.0.0')
        self.sender.start()
        with open("patch.json", "r") as file:
            self.patch = json.load(file)

        # mkae tuple of univeres used in the patch
        universes = set()
        for pixel in self.patch:
            universes.add(self.patch[pixel]['universe'])
        
        # activate output for each universe
        for uni in universes:
            self.sender.activate_output(uni)
            output = self.sender[uni]
            if output is not None:
                output.multicast = True
        
        self.dmx_data = []

        for _ in range(self.num_universes):
            self.dmx_data.append([0] * 512)

        for uni in range(self.num_universes):
            self.sender[uni + 1].dmx_data = self.dmx_data[uni]

    def highlight_pixel(self, pixel: int) -> None:
        """
        Highlights a specific pixel by setting its RGB values to maximum.

        Args:
            pixel (int): The index of the pixel to highlight.

        Returns:
            None
        """

        universe = self.patch[str(pixel)]['universe']
        channels = self.patch[str(pixel)]['channels']

        for i in range(channels):
            self.dmx_data[universe - 1][channels[i + 1]] = 255
        self.send()

    def clear_pixels(self) -> None:
        """
        Clears all the pixels by setting their RGB values to zero.

        Returns:
            None
        """
        for i in range(self.num_universes):
            for j in range(512):
                self.dmx_data[i][j] = 0
        self.send()

    def send(self) -> None:
        """
        Sends the DMX data to the lighting fixtures.

        Returns:
            None
        """
        for i in range(self.num_universes):
            self.sender[i + 1].dmx_data = self.dmx_data[i]

    def stop(self) -> None:
        """
        Stops the sACN sender.

        Returns:
            None
        """
        self.sender.stop()
        self.sender = None