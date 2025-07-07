from flask import Flask, request, jsonify
import os
import base64
import smtplib
from email.message import EmailMessage

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = 'signatures'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set up your Gmail credentials
SENDER_EMAIL = 'captor.fahad@gmail.com'
APP_PASSWORD = 'sqdh zaij xlzx isvw'  # paste your 16-digit app password from Google

RECEIVER_EMAIL = 'captor.fahad@gmail.com'  # you’re sending to yourself

@app.route('/')
def homepage():
    return app.send_static_file('index.html')

@app.route('/save-signature', methods=['POST'])
def save_signature():
    data = request.json
    name = data['name'].strip().replace(" ", "_")
    image_data = data['image'].split(',')[1]
    image_bytes = base64.b64decode(image_data)

    filename = f"{name}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Save the PNG file locally (on Render)
    with open(filepath, 'wb') as f:
        f.write(image_bytes)

    # Send email with PNG attachment
    try:
        msg = EmailMessage()
        msg['Subject'] = f"New Signature Submission: {name}"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg.set_content(f"A new signature was submitted by {name}.")

        with open(filepath, 'rb') as img:
            msg.add_attachment(img.read(), maintype='image', subtype='png', filename=filename)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

        return jsonify({"message": f"Signature saved and emailed to {RECEIVER_EMAIL}!"})

    except Exception as e:
        return jsonify({"message": f"Signature saved but failed to email. Error: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
