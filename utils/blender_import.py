import bpy
import json

# Load the JSON data from the file
file_path = '/Users/mhadley/Dev/Python/pixmap/combined_pixels_blender.json'
with open(file_path, 'r') as file:
    object_data = json.load(file)

# Scaling factor to adjust the size of the coordinates
scale_factor = 0.1  # Adjust this value as needed

# Function to create a sphere at a specified location
def create_sphere(name, location):
    scaled_location = [coord * scale_factor for coord in location]
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=scaled_location)
    sphere = bpy.context.object
    sphere.name = name

# Iterate through the dictionary and create a sphere for each item
for obj_id, coords in object_data.items():
    create_sphere(obj_id, coords)
