import json

import xml.etree.ElementTree as ET

file = "final_map.json"

with open(file, "r") as file:
    pixels = json.load(file)

# Load and parse the XML
tree = ET.parse("maps/MA3_led_px.xml")
root = tree.getroot()

# Calculate the ID offset (assuming it's 9000 based on your description)
id_offset = 9000

# Create lookup dictionary from JSON data, adjusted for the offset
lookup = {(int(k) + id_offset): (int(v["x"]), int(v["y"]), int(v["z"])) for k, v in pixels.items()}

# Update XML based on JSON mappings
for item in root.findall(".//Item"):
    led_id = int(item.get("ID"))
    if led_id in lookup:
        x, y, z = lookup[led_id]
        item.set("X", str(x))
        item.set("Y", str(y))
        item.set("Z", str(z))

# Save the modified XML to a new file
tree.write("modified_led_px.xml")
