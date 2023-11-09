import webcolors

def closest_color(rgb):
    diffs = {}
    for color_hex, color_name in webcolors.CSS3_HEX_TO_NAMES.items():
        r, g, b = webcolors.hex_to_rgb(color_hex)
        diffs[sum([(r - rgb[0])**2,
                   (g - rgb[1])**2,
                   (b - rgb[2])**2])] = color_name
        
    return diffs[min(diffs.keys())]

def convert_to_rgb(hexcode):
    try:
        hexcode = hexcode.replace('"', '').lstrip("#") 
        rgb = tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))
        return rgb
    except ValueError:
        return (0, 0, 0)