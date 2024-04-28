import cv2
import asyncio
from pixmap import Camera
from pixmap import sACN
import json

with open("patch.json", "r") as file:
    patch = json.load(file)

num_pixels = len(patch)
cam = Camera()
acn = sACN()

async def main():
    # Start the camera
    cam.start()

    # Initialize the pixel counter
    pixel_id = 1 

    # Initialize the pixel map dictionary
    pix_map = {}

    # Create a named window and resize it
    cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Webcam", 1280, 720)
    
    input('Press enter to begin mapping')

    for i in range(num_pixels):

        # Highlight the current pixel
        acn.highlight_pixel(pixel_id)

        # Wait for a short period to ensure the signal has reached the pixel
        await asyncio.sleep(0.1)

        # Get the current frame from the camera
        frame = cam.get_frame()

        if frame is not None:

            # Display the frame in the window
            cv2.imshow("Webcam", frame)

            # Get the coordinates of the brightest pixel in the frame
            bright = cam.get_brightest_pixel()

            if bright is not None:
                # Add the coordinates to the pixel map
                pix_map[pixel_id] = bright
                print(f"Pixel {pixel_id}: {bright}")

            # Clear all pixels
            acn.clear_pixels()

            # Increment the pixel counter
            pixel_id += 1

        await asyncio.sleep(0.1)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the VideoCapture object and close the window
    cam.stop()
    acn.stop()
    cv2.destroyAllWindows()

    # Write the pixel map to a JSON file
    with open('pix_map.json', 'w') as file:
        json.dump(pix_map, file)


if __name__ == "__main__":
    asyncio.run(main())
