from flask import Flask, render_template, request
import cv2
import pytesseract
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the request contains an uploaded file
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                # Save the uploaded file
                image_path = 'uploaded_image.png'
                file.save(image_path)
                # Process the image and extract text
                text = image_to_text(image_path)
                # Render the result page with the extracted text
                return render_template('result.html', text=text)
        elif 'text' in request.form:
            text = request.form['text']
            # Render the result page with the entered text
            return render_template('result.html', text=text)
    # Render the main page with the upload form and drawing space
    return render_template('main.html')

def image_to_text(image_path):
    # Load the image using OpenCV
    img = cv2.imread(image_path)
    # check if the given img exists and can be loaded properly
    if img is None:
        return "Failed to load the image. Please check the file path."

    # Preprocess the image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding technique
    block_size = 7  # size of the neighborhood for threshold calculation
    C = 19  # constant subtracted from the mean
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, C)

    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(img)

    # Return the extracted text
    return text

if __name__ == '__main__':
    app.run(debug=True)