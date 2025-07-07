from flask import Flask, request, jsonify
import os
import base64

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = 'signatures'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def homepage():
    return app.send_static_file('index.html')

@app.route('/save-signature', methods=['POST'])
def save_signature():
    data = request.json
    name = data['name'].strip().replace(" ", "_")
    image_data = data['image'].split(',')[1]  # remove base64 header
    image_bytes = base64.b64decode(image_data)

    filename = f"{name}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, 'wb') as f:
        f.write(image_bytes)

    return jsonify({"message": f"Signature saved as {filename}!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

