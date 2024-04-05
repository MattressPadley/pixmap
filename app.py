import cv2
import asyncio
from pixmap import Camera
from pixmap import sACN

cam = Camera()
# acn = sACN(100)

async def main():
    cam.start()


    while True:    
        frame = cam.get_frame()
        if frame is not None:
            cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Webcam", 1280, 720)
            cv2.imshow("Webcam", frame)

            bright = cam.get_brightest_pixel()
            if bright is not None:
                print(bright)
        
        await asyncio.sleep(0.01)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the VideoCapture object and close the window
    cam.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())