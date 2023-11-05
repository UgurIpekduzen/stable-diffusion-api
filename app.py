from flask import Flask, request, render_template, jsonify
from PIL import Image
from io import BytesIO
import base64
import json
import torch

from PIL import Image
from io import BytesIO

assert torch.cuda.is_available()

torch.cuda.empty_cache()

app = Flask(__name__)

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
            img_str = base64.b64encode(buffered.getvalue())
            return jsonify({"ad_image": img_str.decode('utf-8')})
            
            # img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            # return render_template('image.html', gen_image=img_str)

        else:
            return jsonify({"error": "Invalid image format or missing image"})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/generate-ad', methods=['POST'])

def generate_ad():
    try:
        # Get the inputs from the request
        prompt = request.form['prompt']
        logo = request.files['logo']
        punchline = request.form['punchline']
        hexcode = request.form['hexcode']
        button = request.form['button']

        if logo and allowed_file(logo.filename):
            # Convert and process the image
            logo = Image.open(logo)
            logo = logo.convert("RGB")
            logo = logo.resize((768, 768))

            buffered = BytesIO()
            output.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue())
            return jsonify({"ad_image": img_str.decode('utf-8')})
            
            # img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            # return render_template('image.html', gen_image=img_str)

        else:
            return jsonify({"error": "Invalid image format or missing image"})

    except Exception as e:
        return jsonify({"error": str(e)})

# Parameters for the ad template
color = "#316346"
punchline_text = "AI ad banners lead to higher conversations ratesxxxx"
button_text = "Call to action text here! >"


if __name__ == '__main__':
    app.run(debug=True, port=8080)