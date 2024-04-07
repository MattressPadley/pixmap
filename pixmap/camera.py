import cv2
import asyncio
from cv2.typing import MatLike

class Camera():
    """
    Represents a camera object that captures frames from a webcam and performs image processing operations.
    """

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.brightest_pixel = None
        self.frame = None
        self.running = False

    def get_brightest_pixel(self) -> tuple:
        """
        Returns the coordinates of the brightest pixel in the captured frame.

        Returns:
            tuple: The coordinates of the brightest pixel in the format (x, y).
        """
        return self.brightest_pixel
    
    def start(self) -> None:
        """
        Starts capturing frames from the webcam and processing them.
        """
        self.running = True
        asyncio.create_task(self.run())

    def stop(self) -> None:
        """
        Stops capturing frames from the webcam.
        """
        self.running = False
    
    def get_frame(self) -> MatLike:
        """
        Returns the current captured frame.

        Returns:
            MatLike: The current captured frame.
        """
        return self.frame

    async def run(self) -> None:
        """
        Runs the main loop for capturing frames and performing image processing operations.
        """
        if not self.cap.isOpened():
            print("Failed to open camera.")
            return
    
        while self.running:
            # Read the current frame from the webcam
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to read frame.")
                break

            # Draw a crosshair at the brightest pixel in the frame
            self.bright_crosshair(frame)

            # Update the current frame
            self.frame = frame
            await asyncio.sleep(0.01)

    def bright_crosshair(self, frame: MatLike) -> None:
        """
        Draws a crosshair at the brightest pixel in the frame.

        Args:
            frame (MatLike): The frame to draw the crosshair on.
        """
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply a Gaussian blur to the grayscale frame
        blurred = cv2.GaussianBlur(gray, (9, 9), 0)

        # Find the brightest pixel in the blurred image
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(blurred)

        # Update the brightest pixel
        self.brightest_pixel = max_loc

        # Draw two lines that intersect at the brightest pixel
        cv2.line(frame, (max_loc[0], 0), (max_loc[0], frame.shape[0]), (0, 255, 0), 2)
        cv2.line(frame, (0, max_loc[1]), (frame.shape[1], max_loc[1]), (0, 255, 0), 2)

        # Calculate the text position at the intersection of the lines
        text_position = (max_loc[0] + 10, max_loc[1] + 30)

        # Display the coordinates of the brightest pixel on the frame
        cv2.putText(
            frame,
            str(max_loc),
            text_position,
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )