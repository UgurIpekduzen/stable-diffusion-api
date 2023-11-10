from flask import jsonify
import json
import torch
from diffusers import AutoPipelineForImage2Image
from .ad_generator import AdGenerator
from PIL import Image
from .tools import closest_color, convert_to_rgb

# Read the configuration file
with open("config.json") as f:
    cfg = json.loads(f.read())

# Load the model
pipe = AutoPipelineForImage2Image.from_pretrained(cfg['model'], torch_dtype=torch.float16, variant="fp16", use_safetensors=True).to("cuda")

# Set the seed for random number generation
seed = torch.randint(0, 1000000, (1,)).item()
generator = torch.Generator(cfg['device']).manual_seed(seed)

# Generate a new image using the Img2Img algorithm of Stable Diffusion
def generate_img(image, prompt, hexcode):
    """
    Task 1: Stable Diffusion’un Img2Img algoritmasını kullanarak verilen görsele benzer yeni
    bir görsel üretmek. Bunu seçeceğiniz hazır bir modelle yapabilirsiniz. Üretilen görselde
    bizim verdiğimiz bir rengin de kullanılmasını bekliyoruz.
        • Input: Image (png), Prompt (text), Renk (hex code)
        • Output: Image
    """
    try: 
        # Open and convert the input image to RGB format
        image = Image.open(image)
        image = image.convert("RGB")
        
        # Add the provided color to the prompt
        prompt += closest_color(convert_to_rgb(hexcode))
    
        # Generate the new image
        output = pipe(prompt=prompt, image=image, generator=generator).images[0]
        
        return output 
    except Exception as e:
        return jsonify({"error": str(e)})

# Generate a dynamic advertisement template using the generated image and other inputs
def generate_ad(image, logo, hexcode, punchline, button):
    """
    Task 2: Üretilen görseli ve diğer inputları kullanarak basit bir dinamik reklam template’i
    üretmek. En tepede logo, ortada görsel, altında punchline ve en altta button olacak
    şekilde tasarlayabilirsiniz. Button’un ve punchline’ın rengi ayrı bir input olarak verilecek.
    Aşağıdaki örnek görsele çok benzer bir çıktı üretmenizi bekliyoruz.
        • Input: Task 1’deki image, Logo (png), Renk (hex code), Punchline (text), Button (text)
        • Output: Image (png veya svg)
    """

    try: 
        # Create an instance of the AdGenerator class
        ad = AdGenerator()
        
        # Draw the border of the advertisement
        ad.draw_border(hexcode)
        
        # Add the logo, generated image, punchline, and button to the advertisement
        ad.add_logo(logo)
        ad.add_image(image)
        ad.add_punchline(punchline, hexcode)
        ad.add_button(hexcode, button)
        
        # Get the final canvas of the advertisement
        output = ad.get_canvas()

        return output 
    except Exception as e:
        return jsonify({"error": str(e)})