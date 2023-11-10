import webcolors

# This function finds the closest color name in the CSS3 color palette to a given RGB color.
def closest_color(rgb):
    diffs = {}
    for color_hex, color_name in webcolors.CSS3_HEX_TO_NAMES.items():
        r, g, b = webcolors.hex_to_rgb(color_hex)
        # Calculate the Euclidean distance between the RGB values
        diffs[sum([(r - rgb[0])**2,
                   (g - rgb[1])**2,
                   (b - rgb[2])**2])] = color_name
        
    # Return the color name corresponding to the minimum Euclidean distance
    return diffs[min(diffs.keys())]

# This function converts a hex color code to RGB format.
def convert_to_rgb(hexcode):
    try:
        # Remove unnecessary characters and convert to RGB tuple
        hexcode = hexcode.replace('"', '').lstrip("#") 
        rgb = tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))
        return rgb
    except ValueError:
        # Return black in case of an error (invalid hex code)
        return (0, 0, 0)