import cv2
import asyncio
from pixmap import Camera
from pixmap import sACN
import csv


num_pixels = 300
cam = Camera()
acn = sACN(num_pixels)

async def main():
    cam.start()
    pixel = 0
    pix_map = []

    while True:
        frame = cam.get_frame()
        if frame is not None:
            cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Webcam", 1280, 720)
            cv2.imshow("Webcam", frame)

            acn.highlight_pixel(pixel)
            pixel += 1
    

            bright = cam.get_brightest_pixel()
            if bright is not None:
                pix_map.append(bright)

        await asyncio.sleep(.01)
        acn.clear_pixels()

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    
        elif pixel >= num_pixels:
            pixel = 0
            acn.clear_pixels()
            break

    # Release the VideoCapture object and close the window
    cam.stop()
    acn.stop()
    cv2.destroyAllWindows()

    # Write pix_map to a CSV file
    with open('pix_map.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(pix_map)
    

if __name__ == "__main__":
    asyncio.run(main())