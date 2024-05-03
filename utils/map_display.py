import pandas as pd

import matplotlib.pyplot as plt

def plot_points():
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv('pix_map.csv')

    # Extract the x and y coordinates from the DataFrame
    x = df['x']
    y = df['y']

    # Plot the points on a graph with black background and white dots
    plt.scatter(x, y, color='white')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Point Map')
    plt.gca().set_facecolor('black')  # Set the background color to black
    plt.show()

# Call the plot_points function to initially plot the points
plot_points()

# Continuously update the plot when the file changes
while True:
    try:
        # Re-read the CSV file
        df = pd.read_csv('/Users/mhadley/Dev/Python/pixmap/pix_map.csv')

        # Update the plot with the new points
        plt.clf()  # Clear the previous plot
        plt.scatter(df['x'], df['y'], color='white')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Point Map')
        plt.gca().set_facecolor('black')  # Set the background color to black
        plt.pause(1)  # Pause for 1 second before updating the plot
    except FileNotFoundError:
        print("File not found. Make sure the file path is correct.")
        break