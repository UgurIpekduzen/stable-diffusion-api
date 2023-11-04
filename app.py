from flask import Flask, request, render_template, jsonify
from PIL import Image
from io import BytesIO
import base64
import os
import json
import torch
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from diffusers import StableDiffusionImg2ImgPipeline

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

with open("config.json") as f:
    cfg = json.loads(f.read())

assert torch.cuda.is_available()

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(cfg['model'], torch_dtype=torch.float32).to(cfg['device'])

seed = torch.randint(0, 1000000, (1,)).item()
generator = torch.Generator(cfg['device']).manual_seed(seed)

@app.route('/generate-img', methods=['POST'])

def generate_img():
    try:
        # Get the inputs from the request
        prompt = request.form['prompt']
        image = request.files['image']
        hexcode = request.form['hexcode']

        if image and allowed_file(image.filename):
            # Convert and process the image
            image = Image.open(image)
            image = image.convert("RGB")
            image = image.resize((768, 768))

            output = pipe(prompt=prompt, negative_prompt=hexcode, image=image, generator=generator).images[0]

            buffered = BytesIO()
            output.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

            # Render the HTML template and pass the base64 image data
            return render_template('image.html', gen_image=img_str)

        else:
            return jsonify({"error": "Invalid image format or missing image"})

    except Exception as e:
        return jsonify({"error": str(e)})

def draw_canvas():
    # Load the provided images
    generated_image = Image.open("/content/photo2.png")
    logo_image = Image.open("/content/logo1.png")

    punchline_text = "Fırsatları Kaçırmayın, Bugün Keşfedin!"
    button_text = "Keşfet"
    color = "#3498db"

    # Load the provided font

    font_large = ImageFont.truetype(cfg['font-family'], cfg['font-large'])
    font_small = ImageFont.truetype(cfg['font-family'], cfg['font-large'])

    # Create the ad template
    canvas_width = generated_image.width + 150
    canvas_height = generated_image.height + 200
    
    canvas = Image.new('RGB', (canvas_width, canvas_height), tuple(cfg["canvas-color"]))
    draw = ImageDraw.Draw(canvas)

    # Place the logo at the top
    logo_x = (canvas_width - logo_image.width) // 2
    canvas.paste(logo_image, (logo_x, 10))

    # Place the generated image below the logo
    image_x = 80
    image_y = logo_image.height + 20
    canvas.paste(generated_image, (image_x, image_y))

    # Draw the punchline
    text_width, text_height = draw.textsize(punchline_text, font=font_large)
    text_x = (canvas_width - text_width) // 2
    text_y = canvas_height - text_height - 80
    draw.text((text_x, text_y), punchline_text, fill=color, font=font_large)

    # Draw the button
    button_text_width, button_text_height = draw.textsize(button_text, font=font_small)
    button_width = (text_width + 5) / 2
    button_height = text_height + 20
    button_x = (canvas_width - button_width) // 2
    button_y = canvas_height - button_height - 20
    draw.rectangle([button_x, button_y, button_x + button_width, button_y + button_height], fill=color)
    text_x = (canvas_width - button_text_width) // 2
    text_y = button_y + (button_height - button_text_height) // 2
    draw.text((text_x, text_y), button_text, fill="white", font=font_small)

    # Define frame and border properties
    frame_thickness = 1
    border_offset = 20
    border_thickness = 5
    corner_radius = 40

    # Draw the outer frame
    draw.rectangle([frame_thickness, frame_thickness, canvas_width - frame_thickness, canvas_height - frame_thickness], outline="#000000", width=frame_thickness*2)

    # Draw the top rounded border
    top_left = (frame_thickness + border_offset, frame_thickness)
    bottom_right = (canvas_width - frame_thickness - border_offset, frame_thickness + border_thickness)
    draw.rounded_rectangle([top_left, bottom_right], fill=color, radius=corner_radius)

    # Draw the bottom rounded border
    top_left = (frame_thickness + border_offset, canvas_height - frame_thickness - border_thickness)
    bottom_right = (canvas_width - frame_thickness - border_offset, canvas_height - frame_thickness)
    draw.rounded_rectangle([top_left, bottom_right], fill=color, radius=corner_radius)

    # Display the final image
    return canvas

@app.route('/generate-ad', methods=['POST'])

def generate_ad():
    try:
        # Get the inputs from the request
        data = request.json
        logo = Image.open(data['logo']).convert("RGB").resize((768,768))
        image = generate_img()
        hexcode = data['hexcode']
        punchline = data['punchline']
        button = data['button'] 

        response = requests.get(data['image_url'])
        init_image = Image.open(BytesIO(response.content)).convert("RGB")
        init_image = init_image.resize((768, 512))

        image = pipe(prompt=data['prompt'], image=init_image, strength=0.75, guidance_scale=7.5).images
        
        canvas = draw_canvas()
        # Convert the final canvas (ad) to base64 and return
        buffered = BytesIO()
        canvas.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue())
        
        return jsonify({"ad_image": img_str.decode('utf-8')})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=8080)