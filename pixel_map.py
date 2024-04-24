import cv2
import asyncio
from pixmap import Camera
from pixmap import sACN
import csv


num_pixels = 100
cam = Camera()
acn = sACN(num_pixels)

async def main():
    # Start the camera
    cam.start()

    # Initialize the pixel counter
    pixel = 1 

    # Initialize the pixel map list
    pix_map = []

    while True:
        # Get the current frame from the camera
        frame = cam.get_frame()

        if frame is not None:
            # Create a named window and resize it
            cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Webcam", 1280, 720)

            # Display the frame in the window
            cv2.imshow("Webcam", frame)

            # Get the coordinates of the brightest pixel in the frame
            bright = cam.get_brightest_pixel()

            if bright is not None:
                # Add the coordinates to the pixel map
                pix_map.append(bright)

            # Clear all pixels
            acn.clear_pixels()

            # Highlight the current pixel
            acn.highlight_pixel(pixel)

            # Increment the pixel counter
            pixel += 1

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # Reset the pixel counter if it exceeds the number of pixels
        elif pixel >= num_pixels:
            pixel = 0
            acn.clear_pixels()
            break

        # Wait for a short period to ensure the signal has reached the pixel
        await asyncio.sleep(0.1)

    # Release the VideoCapture object and close the window
    cam.stop()
    acn.stop()
    cv2.destroyAllWindows()

    # Write the pixel map to a CSV file
    with open('pix_map.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y'])  # Write column headers
        for pixel in pix_map:
            writer.writerow(pixel)


if __name__ == "__main__":
    asyncio.run(main())
