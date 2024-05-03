import xml.etree.ElementTree as ET
import json

file1 = "scans/20240502161806_side1.json"
file2 = "scans/20240502163608_side2.json"

with open(file1, "r") as file:
    pixels_xy = json.load(file)

with open(file2, "r") as file:
    pixels_yz = json.load(file)


# Load and parse the XML
tree = ET.parse("led_px.xml")
root = tree.getroot()

# Calculate the ID offset (assuming it's 9000 based on your description)
id_offset = 9000

# Create lookup dictionaries from JSON data, adjusted for the offset
xy_lookup = {(int(k) + id_offset): (int(v[0]), int(v[1])) for k, v in pixels_xy.items()}
yz_lookup = {
    (int(k) + id_offset): int(v[0]) for k, v in pixels_yz.items()
}  # Adjusted to store only the Z value

# Update XML based on JSON mappings
for item in root.findall(".//Item"):
    led_id = int(item.get("ID"))
    if led_id in xy_lookup:
        x, y = xy_lookup[led_id]
        item.set("X", str(x))
        item.set("Y", str(y))

    if led_id in yz_lookup:
        z = yz_lookup[led_id]
        item.set("Z", str(z))

# Save the modified XML to a new file
tree.write("modified_led_px.xml")
