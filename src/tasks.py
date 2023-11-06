
from flask import jsonify
import json
import torch
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline
from .ad_generator import AdGenerator
import json

with open("config.json") as f:
    cfg = json.loads(f.read())

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(cfg['model'], torch_dtype=torch.float32).to(cfg['device'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(cfg['allowed_extensions'])

seed = torch.randint(0, 1000000, (1,)).item()
generator = torch.Generator(cfg['device']).manual_seed(seed)

def generate_img(prompt, image, hexcode):
    try: 
        if image and allowed_file(image.filename):
            # Convert and process the image
            image = Image.open(image)
            image = image.convert("RGB")
            output = pipe(prompt=prompt, negative_prompt=hexcode, image=image, generator=generator).images[0]
            
            return output
    except Exception as e:
        return jsonify({"error": str(e)})

def generate_ad(image, logo, hexcode, punchline, button):
    try: 
        if logo and allowed_file(logo.filename):
            image = Image.open(image)
            ad = AdGenerator(image)
            ad.draw_border(hexcode)
            ad.add_logo(logo)
            ad.add_image(image)
            ad.add_punchline(punchline, hexcode)
            ad.add_button(hexcode, button)
            output = ad.get_canvas()

            return output
    except Exception as e:
        return jsonify({"error": str(e)})