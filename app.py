from flask import Flask, request, send_file, render_template
import torch
import os
from src.tasks import generate_ad, generate_img
import json

assert torch.cuda.is_available()
torch.cuda.empty_cache()

with open("config.json") as f:
    cfg = json.loads(f.read())

app = Flask(__name__, template_folder='./templates/')
app.config['UPLOAD_FOLDER'] = cfg['image_upload_folder']

@app.route('/images/<filename>')
def show_result(filename):
    return send_file(os.path.join(cfg['image_upload_folder'], filename), mimetype='image/png')

@app.route('/download/<filename>')
def download_result(filename):
    return send_file(os.path.join(cfg['image_upload_folder'], filename), as_attachment=True)

@app.route('/', methods=['GET', 'POST'])
def img2img_api():
    if request.method == 'POST':

        prompt = request.form['prompt']
        image = request.files['image']
        aiimg_hexcode = request.form['aiimg_hexcode']
        logo = request.files['logo']
        adimg_hexcode = request.form['adimg_hexcode']
        punchline = request.form['punchline']
        button = request.form['button']

        gen_image = generate_img(image, prompt, aiimg_hexcode)
        gen_img_path = os.path.join(cfg['image_upload_folder'], cfg['gen_img_name'])
        gen_image.save(gen_img_path)
        
        ad_image = generate_ad(gen_img_path, logo, adimg_hexcode, punchline, button)
        ad_img_path = os.path.join(cfg['image_upload_folder'], cfg['ad_img_name'])
        ad_image.save(ad_img_path)
        
        return render_template('result.html', result=cfg['ad_img_name'])
    else:
        return render_template('index.html')
