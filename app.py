# from flask import Flask, request, jsonify, send_file, Response
# from PIL import Image
# from io import BytesIO
# import base64
# import torch

# from PIL import Image
# from io import BytesIO
# from tasks import generate_ad, generate_img

# assert torch.cuda.is_available()

# torch.cuda.empty_cache()

# app = Flask(__name__)

# @app.route('/img2img-api', methods=['POST'])

# def img2img_api():
#     try:
#         # Get the inputs from the request
#         prompt = request.form['prompt']
#         image = request.files['image']
#         aiimg_hexcode = request.form['aiimg_hexcode']
        
#         # logo = request.files['logo']
#         # adimg_hexcode = request.form['adimg_hexcode']
#         # punchline = request.form['punchline']
#         # button = request.form['button']

#         gen_image = generate_img(image=image, prompt=prompt, hexcode=aiimg_hexcode)
#         if gen_image:
#             output_buffer = BytesIO()
#             gen_image.save(output_buffer, format="PNG")
#             response = Response(output_buffer.getvalue(), mimetype="image/png")
#             return response
#         else:
#             return jsonify({"error": "Image generation failed."})
#         # img_name = generate_ad(image=gen_image, logo=logo, hexcode=adimg_hexcode, punchline=punchline, button=button)
        
#         # return send_file('image.html', gen_image=img_name)

#     except Exception as e:
#         return jsonify({"error": str(e)})
# if __name__ == '__main__':
#     app.run(debug=True, port=8080)
# # @app.route('/generate-ad', methods=['POST'])

# # def generate_ad():
# #     try:
# #         # Get the inputs from the request
# #         prompt = request.form['prompt']
# #         logo = request.files['logo']
# #         punchline = request.form['punchline']
# #         hexcode = request.form['hexcode']
# #         button = request.form['button']

# #         if logo and allowed_file(logo.filename):
# #             # Convert and process the image
# #             logo = Image.open(logo)
# #             logo = logo.convert("RGB")
# #             logo = logo.resize((768, 768))

# #             buffered = BytesIO()
# #             output.save(buffered, format="PNG")
# #             img_str = base64.b64encode(buffered.getvalue())
# #             return jsonify({"ad_image": img_str.decode('utf-8')})
            
# #             # img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
# #             # return render_template('image.html', gen_image=img_str)

# #         else:
# #             return jsonify({"error": "Invalid image format or missing image"})

# #     except Exception as e:
# #         return jsonify({"error": str(e)})

# # Parameters for the ad template


# if __name__ == '__main__':
#     app.run(debug=True, port=8080)

from flask import Flask, request, jsonify, send_file
import torch
import os

from src.tasks import generate_ad, generate_img

assert torch.cuda.is_available()
torch.cuda.empty_cache()

app = Flask(__name__)

@app.route('/img2img-api', methods=['POST'])
def img2img_api():
    try:
        # Get the inputs from the request
        # prompt = request.form['prompt']
        image = request.files['image']
        # aiimg_hexcode = request.form['aiimg_hexcode']
        logo = request.files['logo']
        adimg_hexcode = request.form['adimg_hexcode']
        punchline = request.form['punchline']
        button = request.form['button']
    
        # gen_image = generate_img(image=image, prompt=prompt, hexcode=aiimg_hexcode)
        img_name = generate_ad(image=image, logo=logo, hexcode=adimg_hexcode, punchline=punchline, button=button)

        if img_name:
            save_path = os.path.join("images", "ad_image.png")
            img_name.save(save_path)
            return send_file(save_path, mimetype="image/png")
        else:
            return jsonify({"error": "Image generation failed."})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=8080)