import json 

files = [
    "20240527151949_side1.json",
    "20240527153303_side2.json",
    "20240527154318_side3.json",
    "20240527155436_side4.json",
]

raw_maps = {}
for file in files:
    filename = f"scans/{file}"
    side = file.split("_")[1].split(".")[0]
    with open(filename, "r") as f:
        raw_maps[side] = json.load(f)

final_map = {}
pixel_count = 2000

for i in range(pixel_count):

    index = str(i + 1)
    final_map[index] = {}
    # compare x Brightness
    if raw_maps["side1"][index]["brightness"] > raw_maps["side3"][index]["brightness"]:
        final_map[index]["x"] = raw_maps["side1"][index]["x"]
    else:
        final_map[index]["x"] = 1080 - int(raw_maps["side3"][index]["x"])

    # compare z Brightness
    if raw_maps["side2"][index]["brightness"] > raw_maps["side4"][index]["brightness"]:
        final_map[index]["z"] = raw_maps["side2"][index]["z"]
    else:
        final_map[index]["z"] = 1080 - int(raw_maps["side4"][index]["z"])

    # compare y Brightness
    if raw_maps["side1"][index]["brightness"] > raw_maps["side2"][index]["brightness"]:
        y1_bright = raw_maps["side1"][index]
    else:
        y1_bright = raw_maps["side2"][index]

    if raw_maps["side3"][index]["brightness"] > raw_maps["side4"][index]["brightness"]:
        y2_bright = raw_maps["side3"][index]
    else:
        y2_bright = raw_maps["side4"][index]

    if y1_bright["brightness"] > y2_bright["brightness"]:
        final_map[index]["y"] = y1_bright["y"]
    else:
        final_map[index]["y"] = y2_bright["y"]

# Save final_map to a JSON file
with open("final_map.json", "w") as f:
    json.dump(final_map, f)

print("Final map saved to final_map.json")
