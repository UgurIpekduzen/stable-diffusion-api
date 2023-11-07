# import json
# import torch
# from PIL import Image
# from diffusers import StableDiffusionImg2ImgPipeline
# import os 

# assert torch.cuda.is_available()
# torch.cuda.empty_cache()

# with open("config.json") as f:
#     cfg = json.loads(f.read())

# pipe = StableDiffusionImg2ImgPipeline.from_pretrained(cfg['model'], torch_dtype=torch.float32).to(cfg['device'])

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(cfg['allowed_extensions'])

# seed = torch.randint(0, 1000000, (1,)).item()
# generator = torch.Generator(cfg['device']).manual_seed(seed)
    
# prompt = "A coffee cup on a table with flowers, ghibli style, 8k, detailed, high resolution"
# image = "coffee_cup.jpg"
# aiimg_hexcode = "#3498db"
# logo = "logo.png"
# adimg_hexcode = "#316346"
# punchline = "AI ad banners lead to higher conversations ratesxxxx"
# button = "Call to action text here! >"

# image = Image.open(image)
# image = image.convert("RGB")
# output = pipe(prompt=prompt, negative_prompt=aiimg_hexcode, image=image, generator=generator).images[0]

# save_path = os.path.join("images", "generated.png")
# output.save(save_path)

from scipy.spatial import KDTree
import webcolors  

def convert_rgb_to_names(rgb_tuple):
    
    # a dictionary of all the hex and their respective names in css3
    css3_db = webcolors.CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(webcolors.hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)
    _ , index = kdt_db.query(rgb_tuple)
    return names[index]

# def closest_color(rgb):
#     diffs = {}
#     for color_hex, color_name in CSS3_HEX_TO_NAMES.items():
#         r, g, b = hex_to_rgb(color_hex)
#         diffs[sum([(r - rgb[0])**2,
#                    (g - rgb[1])**2,
#                    (b - rgb[2])**2])] = color_name
        
#     return diffs[min(diffs.keys())]
# def hex_to_rgb(hexcode):
#     try:
#         # Hex renk kodundan gereksiz karakterleri kaldırın ve doğrudan RGB'ye çevirin
#         hexcode = hexcode.replace('"', '').lstrip("#") 
#         rgb = tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))
#         return rgb
#     except ValueError:
#         # Hata durumunda varsayılan bir değer döndürün (örneğin siyah renk: (0, 0, 0))
#         return (0, 0, 0)

# print(hex_to_rgb("#316346"))
print(convert_rgb_to_names((49, 99, 70)))
# print(closest_color((49, 99, 70)))
# print(rgb_to_name(hex_to_rgb("#316346")))