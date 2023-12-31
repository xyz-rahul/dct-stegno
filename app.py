from flask import Flask,request,send_file, render_template, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from io import BytesIO


from dct import DCT

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # Your existing logic for index route goes here

        return render_template('index.html',decoded_message=None, error_message=None)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('index.html',decoded_message=None, error_message=error_message)


upload = ''
app.config['UPLOAD'] = upload


@app.route('/encode', methods=['POST'])
def file_encode():
    message = request.form.get('message')
    print("messsss ",message)
    f = request.files['image']
    filename = secure_filename(f.filename)
    file_content = f.read()

    # Convert the file content to a NumPy array
    nparr = np.frombuffer(file_content, np.uint8)

    # Decode the image using cv2
    uploaded_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


    # ENCODE

    try:
        # Input for the image file (can still use the original code)
        original_image_file = filename  # You can also use input("Enter the name of the file with extension: ")

        # Continue with the encoding process
        dct_img_encoded = DCT().encode_image(uploaded_image, message)
        dct_encoded_image_file = "dct_" + filename

        success, encoded_img = cv2.imencode('.png',dct_img_encoded)
        # send_file(as_attachment=True,download_name='dct_babylon.png')
        if success:
            # Convert the encoded data to bytes
            encoded_bytes = encoded_img.tobytes()

            # Return the encoded image as a response
            return send_file(
                BytesIO(encoded_bytes),
                mimetype='image/png',
                as_attachment=True,
                download_name='encoded_image.png'
            )
        else:
            return "Error encoding image."

    except Exception as e:
        return jsonify(error=f"An error occurred: {str(e)}")


@app.route('/decode', methods=['POST'])
def file_decode():
    f = request.files['image']
    filename = secure_filename(f.filename)
    file_content = f.read()

    # Convert the file content to a NumPy array
    nparr = np.frombuffer(file_content, np.uint8)

    # Decode the image using cv2
    uploaded_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # ENCODE

    try:
        # Continue with the encoding process
        msg = DCT().decode_image(uploaded_image)

        print("secret: ",msg)
        # Pass the decoded message to the template
        return render_template('index.html', decoded_message=msg, error_message=None)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('index.html', decoded_message=None, error_message=error_message)

    

