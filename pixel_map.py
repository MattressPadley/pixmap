import cv2
import asyncio
from pixmap import Camera
from pixmap import sACN
import csv
import websockets

num_pixels = 100
cam = Camera()
acn = sACN(num_pixels)


async def handle_connection(websocket, path):
    # Start the camera
    cam.start()

    # Initialize the pixel counter
    pixel = 1

    # Initialize the pixel map list
    pix_map = []

    try:
        while True:
            # Get the current frame from the camera
            frame = cam.get_frame()

            if frame is not None:
                frame = cv2.resize(frame, (1280, 720))
                # Encode the frame as a JPEG image
                _, jpeg = cv2.imencode(".jpg", frame)

                # Send the JPEG data over the WebSocket connection
                await websocket.send(jpeg.tobytes())

            # Clear all pixels
            acn.clear_pixels()

            # Highlight the current pixel
            # acn.highlight_pixel(pixel)

            # Increment the pixel counter
            #pixel += 1

            # Wait for a short period to ensure the signal has reached the pixel
            await asyncio.sleep(0.03)

            # Break the loop if the 'q' key is pressed
            #
            # Reset the pixel counter if it exceeds the number of pixels
            # elif pixel >= num_pixels:
            #     pixel = 0
            #     acn.clear_pixels()
            #     break

    finally:
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


async def main():
    # Create a WebSocket server
    server = await websockets.serve(handle_connection, "localhost", 8765)

    # Start the server
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
