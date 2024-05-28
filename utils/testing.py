from pixmap import sACN
import json
import time

acn = sACN()

with open("final_map.json", "r") as file:
    pixels = json.load(file)

sorted_pixels = sorted(pixels.items(), key=lambda x: x[1]["x"])

while True:
    for pixel in sorted_pixels:
        acn.highlight_pixel(pixel[0])
        # time.sleep(0.01)

        # input("Press enter to continue")
    time.sleep(0.5)
    acn.clear_pixels()
