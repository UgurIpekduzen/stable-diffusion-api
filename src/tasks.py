
import json
import torch
from PIL import Image
from io import BytesIO
from diffusers import StableDiffusionImg2ImgPipeline
from ad_generator import AdGenerator

with open("config.json") as f:
    cfg = json.loads(f.read())

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(cfg['model'], torch_dtype=torch.float32).to(cfg['device'])

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(cfg['allowed_extensions'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

seed = torch.randint(0, 1000000, (1,)).item()
generator = torch.Generator(cfg['device']).manual_seed(seed)

def generate_img(prompt, image, hexcode):

    if image and allowed_file(image.filename):
        # Convert and process the image
        image = Image.open(image)
        image = image.convert("RGB")
        image = image.resize((768, 768))

        output = pipe(prompt=prompt, negative_prompt=hexcode, image=image, generator=generator).images[0]

        buffered = BytesIO()
        output.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue())
        return jsonify({"ad_image": img_str.decode('utf-8')})
        
        # img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        # return render_template('image.html', gen_image=img_str)

    else:
        return jsonify({"error": "Invalid image format or missing image"})

    
def generate_ad(image, logo, hexcode, punchline, button):

    if logo and allowed_file(logo.filename):
        # Convert and process the image
        logo = Image.open(logo)
        logo = logo.convert("RGB")
        logo = logo.resize((768, 768))
        
        ad = AdGenerator(image)
        ad.draw_border(hexcode)
        ad.add_logo("logo1.png")
        ad.add_image("photo1.png")
        ad.add_punchline(punchline, text_color=hexcode)
        ad.add_button(hexcode, button)

        buffered = BytesIO()
        output.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue())
        return jsonify({"ad_image": img_str.decode('utf-8')})
        
        # img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        # return render_template('image.html', gen_image=img_str)

    else:
        return jsonify({"error": "Invalid image format or missing image"})