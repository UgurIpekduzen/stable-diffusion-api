from flask import Flask, request, jsonify, send_file, render_template
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
# @app.route('/generate-image', methods=['POST'])

# def generate_image():
#     try:
#         prompt = request.form['prompt']
#         image = request.files['image']
#         aiimg_hexcode = request.form['aiimg_hexcode']
        
#         gen_image = generate_img(image, prompt, aiimg_hexcode)

#         save_path = os.path.join(cfg['image_path'], cfg['gen_img_name'])
#         gen_image.save(save_path)
        
#         return send_file(save_path, mimetype="image/png")
#     except Exception as e:
#         return jsonify({"error": str(e)})  
    
# @app.route('/img2img-api', methods=['POST'])
# def img2img_api():
#     try:
#         # Get the inputs from the request
#         prompt = request.form['prompt']
#         image = request.files['image']
#         aiimg_hexcode = request.form['aiimg_hexcode']
#         logo = request.files['logo']
#         adimg_hexcode = request.form['adimg_hexcode']
#         punchline = request.form['punchline']
#         button = request.form['button']

#         gen_image = generate_img(image, prompt, aiimg_hexcode)
#         ad_image = generate_ad(gen_image, logo, adimg_hexcode, punchline, button)

#         save_path = os.path.join(cfg['image_path'], cfg['ad_img_name'])
#         ad_image.save(save_path)
        
#         return send_file(save_path, mimetype="image/png")
#     except Exception as e:
#         return jsonify({"error": str(e)})

@app.route('/images/<filename>')

def show_result(filename):
    return send_file(os.path.join(cfg['image_upload_folder'], filename), mimetype='image/png')

@app.route('/img2img-api', methods=['GET', 'POST'])
def img2img_api():
    if request.method == 'POST':
         # Get the inputs from the request
        prompt = request.form['prompt']
        image = request.files['image']
        aiimg_hexcode = request.form['aiimg_hexcode']
        logo = request.files['logo']
        adimg_hexcode = request.form['adimg_hexcode']
        punchline = request.form['punchline']
        button = request.form['button']

        gen_image = generate_img(image, prompt, aiimg_hexcode)
        ad_image = generate_ad(gen_image, logo, adimg_hexcode, punchline, button)

        ad_img_path = os.path.join(cfg['image_upload_folder'], cfg['ad_img_name'])
        ad_image.save(ad_img_path)
        
        return render_template('result.html', result=cfg['ad_img_name'])
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8080)
