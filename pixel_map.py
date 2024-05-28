import cv2
import asyncio
from pixmap import Camera
from pixmap import sACN
import json
import datetime

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
    
    side_num = int(input("Enter the number of the side of the object you're scanning: "))
    input('Press enter to begin mapping')

    for i in range(num_pixels):

        # Highlight the current pixel
        acn.highlight_pixel(pixel_id)

        # Wait for a short period to ensure the signal has reached the pixel
        await asyncio.sleep(0.2)

        # Get the current frame from the camera
        frame = cam.get_frame()

        if frame is not None:

            # Display the frame in the window
            cv2.imshow("Webcam", frame)

            # Get the coordinates of the brightest pixel in the frame
            bright, max = cam.get_brightest_pixel()

            if side_num == 1:
                dim1 = "y"
                dim2 = "x"
            elif side_num == 2:
                dim1 = "y"
                dim2 = "z"
            elif side_num == 3:
                dim1 = "y"
                dim2 = "x"
            elif side_num == 4:
                dim1 = "y"
                dim2 = "z"

            if bright is not None:
                # Add the coordinates to the pixel map
                pixel = {
                    dim1: bright[0],
                    dim2: bright[1],
                    "brightness": max
                }
                pix_map[pixel_id] = pixel
                print(f"Pixel {pixel_id}: {bright} - Brightness: {max}")

            # Clear all pixels
            acn.clear_pixels()

            # Increment the pixel counter
            pixel_id += 1

        #await asyncio.sleep(0.01)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the VideoCapture object and close the window
    cam.stop()
    acn.stop()
    cv2.destroyAllWindows()

    # Generate a unique filename based on current datetime and side_num
    filename = f"scans/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_side{side_num}.json"

    # Write the pixel map to a JSON file with the generated filename
    with open(filename, 'w') as file:
        json.dump(pix_map, file)


if __name__ == "__main__":
    asyncio.run(main())
