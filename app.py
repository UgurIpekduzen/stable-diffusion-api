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

app = Flask(__name__)

with open("config.json") as f:
    cfg = json.loads(f.read())

assert torch.cuda.is_available()

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(cfg['model'], torch_dtype=torch.float32).to(cfg['device'])

@app.route('/generate-image', methods=['POST'])

def generate_ad():
    try:
        # Get the inputs from the request
        data = request.json

        response = requests.get(data['image_url'])
        init_image = Image.open(BytesIO(response.content)).convert("RGB")
        init_image = init_image.resize((768, 512))

        image = pipe(prompt=data['prompt'], image=init_image, strength=0.75, guidance_scale=7.5).images
        
        return jsonify({"ad_image": img_str.decode('utf-8')})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)

# app = Flask(__name__, template_folder='templates')

# UPLOAD_FOLDER = 'uploads'

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/')
# def upload_form():
#     return render_template('upload.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return "Dosya seçilmedi!"

#     file = request.files['file']

#     if file.filename == '':
#         return "Dosya adı boş!"

#     if file and allowed_file(file.filename):
#         filename = file.filename
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return "Dosya yüklendi: " + filename
#     else:
#         return "Geçersiz dosya türü!"

# if __name__ == '__main__':
#     app.run(debug=True)