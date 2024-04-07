import cv2
import asyncio
from pixmap import Camera
from pixmap import sACN
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.num_pixels = 100
        self.cam = Camera()
        self.acn = sACN(self.num_pixels)

        self.pixel_input = QLineEdit()
        self.start_button = QPushButton("Start")
        self.preview_label = QLabel()

        self.init_ui()

    def init_ui(self):
        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Number of Pixels:"))
        layout.addWidget(self.pixel_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.preview_label)
        self.setLayout(layout)

        # Connect the button click event to the start function
        self.start_button.clicked.connect(self.start)

    def start_preview(self):
        # Set up the camera preview
        self.cam.start()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_preview)
        self.timer.start(30)  # Update the preview every 30 milliseconds

    def start(self):
        # Get the number of pixels from the input field
        self.num_pixels = int(self.pixel_input.text())
        self.acn = sACN(self.num_pixels)

        # Start the main loop
        asyncio.create_task(self.map_pixels())

    async def map_pixels(self):
        # Initialize the pixel counter
        pixel = 1

        # Initialize the pixel map list
        pix_map = []

        while True:
            # Get the current frame from the camera
            frame = self.cam.get_frame()

            if frame is not None:
                # Display the frame in the preview label
                self.display_frame(frame)

                # Get the coordinates of the brightest pixel in the frame
                bright = self.cam.get_brightest_pixel()

                if bright is not None:
                    # Add the coordinates to the pixel map
                    pix_map.append(bright)

                # Clear all pixels
                self.acn.clear_pixels()

                # Highlight the current pixel
                self.acn.highlight_pixel(pixel)

                # Increment the pixel counter
                pixel += 1

                # Wait for a short period to ensure the signal has reached the pixel
                await asyncio.sleep(0.5)

            # Break the loop if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            # Reset the pixel counter if it exceeds the number of pixels
            elif pixel >= self.num_pixels:
                pixel = 0
                self.acn.clear_pixels()
                break

        # Release the VideoCapture object
        self.cam.stop()
        self.acn.stop()

        # Write the pixel map to a CSV file
        with open('pix_map.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['x', 'y'])  # Write column headers
            for pixel in pix_map:
                writer.writerow(pixel)

    def display_frame(self):
        # Get the current frame from the camera
        frame = self.cam.get_frame()

        # Convert the frame from BGR to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame to a QImage
        image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)

        # Convert the QImage to a QPixmap
        pixmap = QPixmap.fromImage(image)

        # Set the pixmap as the pixmap of the preview label
        self.preview_label.setPixmap(pixmap)

    def update_preview(self):
        # Get the current frame from the camera
        frame = self.cam.get_frame()

        if frame is not None:
            # Display the frame in the preview label
            self.display_frame(frame)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    window.start_preview()
    app.exec_()
