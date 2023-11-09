from flask import jsonify
import json
import torch
from diffusers import AutoPipelineForImage2Image
from .ad_generator import AdGenerator
from PIL import Image
from .editing import closest_color, convert_to_rgb

with open("config.json") as f:
    cfg = json.loads(f.read())

pipe = AutoPipelineForImage2Image.from_pretrained(cfg['model'], torch_dtype=torch.float16, variant="fp16", use_safetensors=True).to("cuda")

seed = torch.randint(0, 1000000, (1,)).item()
generator = torch.Generator(cfg['device']).manual_seed(seed)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(cfg['allowed_extensions'])

def generate_img(image, prompt, hexcode):
    try: 
        image = Image.open(image)
        image = image.convert("RGB")
        
        prompt += closest_color(convert_to_rgb(hexcode))
        
        output = pipe(prompt=prompt 
                        ,image=image, generator=generator 
                        # ,strength=cfg['strength'], 
                        # ,guidance_scale=cfg['guidance_scale']
                    ).images[0]
        
        return output 
    except Exception as e:
        return jsonify({"error": str(e)})

def generate_ad(image, logo, hexcode, punchline, button):
    try: 
        ad = AdGenerator()
        ad.draw_border(hexcode)
        ad.add_logo(logo)
        ad.add_image(image)
        ad.add_punchline(punchline, hexcode)
        ad.add_button(hexcode, button)
        output = ad.get_canvas()

        return output 
    except Exception as e:
        return jsonify({"error": str(e)})
