import cv2
import time

class Camera():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.brightest_pixel = None
        self.width = 1280
        self.height = 720

    def get_brightest_pixel(self):
        return self.brightest_pixel

    def run(self):
        while True:
            # Read the current frame from the webcam
            ret, frame = self.cap.read()

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

            # Display the frame in a window named "Webcam" with adjustable size
            cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Webcam", self.width, self.height)
            cv2.imshow("Webcam", frame)

            # Break the loop if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release the VideoCapture object and close the window
        self.cap.release()
        cv2.destroyAllWindows()
