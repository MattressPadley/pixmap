import json

file_1 = "scans/20240502161806_side1.json"
file_2 = "scans/20240502163608_side2.json"

with open(file_1, "r") as file:
    pixels_xy = json.load(file)

with open(file_2, "r") as file:
    pixels_zy = json.load(file)


combined_pixels = {}
for id, xy in pixels_xy.items():
    if id in pixels_zy:
        z = pixels_zy[id][0]
        combined_pixels[id] = [xy[0], xy[1], z]  # Convert z to a list

with open("combined_pixels_blender.json", "w") as file:
    json.dump(combined_pixels, file, indent=4)