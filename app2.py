from flask import Flask, request, jsonify, send_file
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

# Define the API endpoint
@app.route('/generate-ad', methods=['POST'])
def generate_ad():
    try:
        # Get the inputs from the request
        data = request.json
        prompt = data['prompt']
        init_image_base64 = data['init_image']
        logo_image_base64 = data['logo_image']
        
        # Convert base64 to Image
        init_image = Image.open(BytesIO(base64.b64decode(init_image_base64)))
        logo_image = Image.open(BytesIO(base64.b64decode(logo_image_base64)))
        
        # ...[The rest of the provided code to generate the ad]...

        # Convert the final canvas (ad) to base64 and return
        buffered = BytesIO()
        canvas.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue())
        
        return jsonify({"ad_image": img_str.decode('utf-8')})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=8080)