import json

def patch_strip(pixel_id, num_pixels, channels_per_pixel, start_address, start_universe=1) -> tuple[dict,int]:
    """
    Generates a DMX patch for a strip of pixels.

    Args:
        pixel_id (int): The starting pixel ID.
        num_pixels (int): The number of pixels in the strip.
        channels_per_pixel (int): The number of DMX channels per pixel.
        start_address (int): The starting DMX address.
        start_universe (int, optional): The starting DMX universe. Defaults to 1.

    Returns:
        tuple[dict,int]: A tuple containing the DMX patch map (dictionary) and the updated pixel ID (int).
    """

    max_channels_per_universe = 512
    dmx_map = {}
    current_universe = start_universe
    current_channel = start_address

    for _ in range(num_pixels):
        if current_channel + channels_per_pixel - 1 > max_channels_per_universe:
            current_universe += 1
            current_channel = 1  # Reset channel to start in new universe
        
        channels = tuple(range(current_channel, current_channel + channels_per_pixel))

        dmx_map[pixel_id] = {
            "universe": current_universe,
            "channels": channels,
        }
        current_channel += channels_per_pixel
        pixel_id += 1

    return dmx_map, pixel_id

def main():
    """
    Main function to interactively create and store DMX Patches.

    This function prompts the user to enter the number of pixels, number of channels per pixel,
    start address, and start universe for each strip. It then calls the `patch_strip` function
    to generate a strip map and updates the main DMX map with the current strip map. The user
    can choose to add more strips or exit the program.

    Finally, the main DMX map is written to a JSON file named "dmx_map.json".

    Args:
        None

    Returns:
        None
    """

    dmx_map = {}  # Single dictionary to store all the DMX maps
    pixel_id = 1  # Start from pixel ID 1
    num_pixels = int(input("Enter the number of pixels: "))
    channels_per_pixel = int(input("Enter the number of channels per pixel: "))

    while True:
        start_address = input("Enter the start address: ")
        start_universe, start_channel = map(int, start_address.split("."))

        strip_map, pixel_id = patch_strip(pixel_id, num_pixels, channels_per_pixel, start_channel, start_universe)
        dmx_map.update(strip_map)  # Update the main DMX map with the current strip map

        choice = input("Do you want to add more strips? (y/n): ")
        if choice.lower() != "y":
            break

    with open("patch.json", "w") as f:
        json.dump(dmx_map, f)  # Write the main DMX map to the file


if __name__ == "__main__":
    main()
