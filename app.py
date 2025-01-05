import os
from flask import Flask, request, jsonify, render_template, url_for
import tensorflow as tf
from PIL import Image
from dotenv import load_dotenv
import openai

# Load environment variables from the .env file
load_dotenv()

# Access the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask App
app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load MobileNetV2 Model
model = tf.keras.applications.mobilenet_v2.MobileNetV2(weights='imagenet')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        # Get the uploaded image file
        image_file = request.files['image']
        if not image_file:
            return render_template('index.html', error="No image provided.")

        # Save the uploaded image
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_path)

        # Process the uploaded image
        image = Image.open(image_path)
        image = image.convert('RGB')  # Ensure the image is in RGB mode
        image = image.resize((224, 224))  # Resize to the required input size for MobileNetV2
        image_array = tf.keras.preprocessing.image.img_to_array(image)
        image_array = tf.keras.applications.mobilenet_v2.preprocess_input(image_array)
        image_array = tf.expand_dims(image_array, axis=0)

        # Predict the scene
        predictions = model.predict(image_array)
        label = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=1)[0][0][1]

        # Use OpenAI to generate enhancement suggestions
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert photography assistant."},
                {"role": "user", "content": f"Provide photography tips for a scene containing {label}. Include each tip as a separate line in a numbered or bullet-point format."}
            ]
        )
        suggestions = response.choices[0].message["content"].strip()

        # Normalize suggestions
        suggestions_list = [
            s.lstrip("1234567890.- ").strip() for s in suggestions.split("\n") if s.strip()
        ]

        # Render the result page with the image and suggestions
        return render_template(
            'result.html',
            description=f"This image appears to contain: {label}.",
            suggestions=suggestions_list,
            image_url=url_for('static', filename=f'uploads/{image_file.filename}')
        )

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
