from flask import Flask, render_template, request, redirect, send_file
from stegano import lsb
import os

app = Flask(__name__)
print(os.getcwd())
# Path to the uploads folder
UPLOADS_FOLDER = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        # Get the uploaded image file
        image_file = request.files['image']
        if image_file:
            # Save the uploaded image file
            image_path = os.path.join(UPLOADS_FOLDER, image_file.filename)
            image_file.save(image_path)

            # Get the message to encrypt
            message = request.form['message']

            # Encrypt the message and save the image
            encrypted_image = lsb.hide(image_path, message)
            encrypted_image_path = os.path.join(UPLOADS_FOLDER, 'encrypted_image.png')
            encrypted_image.save(encrypted_image_path)

            # Provide the encrypted image for download
            return send_file(encrypted_image_path, as_attachment=True)

    return render_template('encrypt.html')

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        # Get the uploaded image file
        image_file = request.files['image']
        if image_file:
            # Save the uploaded image file
            image_path = os.path.join(UPLOADS_FOLDER, image_file.filename)
            image_file.save(image_path)

            # Decrypt the hidden message from the image
            decrypted_message = lsb.reveal(image_path)

            # Delete the uploaded image file
            os.remove(image_path)

            return render_template('decrypt.html', decrypted_message=decrypted_message)

    return render_template('decrypt.html')

@app.after_request
def remove_uploaded_files(response):
    # Delete all files in the uploads folder
    for filename in os.listdir(UPLOADS_FOLDER):
        file_path = os.path.join(UPLOADS_FOLDER, filename)
        os.remove(file_path)

    return response

if __name__ == '__main__':
    app.run(debug=True)
