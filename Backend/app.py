from flask import Flask, request, jsonify
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ Define Waste Categories
BIODEGRADABLE = ['cardboard', 'paper', 'trash']
NON_BIODEGRADABLE = ['glass', 'metal', 'plastic']
CLASSES = BIODEGRADABLE + NON_BIODEGRADABLE  # 6 classes

# ✅ Load the Model
MODEL_PATH = "waste_classifier.h5"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model file '{MODEL_PATH}' not found.")
model = load_model(MODEL_PATH)
print("✅ Model loaded successfully with 6 classes!")

# ✅ Image Preprocessing Function
def preprocess_image(img):
    img = cv2.resize(img, (224, 224))  # Resize image to match model input
    print("🔍 Image shape after resizing:", img.shape)

    # Debug: Print pixel range before normalization
    print("🔍 Image pixel range before normalization:", img.min(), img.max())

    img = img.astype("float32") / 255.0  # Normalize to 0-1

    # Debug: Print pixel range after normalization
    print("✅ Image pixel range after normalization:", img.min(), img.max())

    img = np.expand_dims(img, axis=0)  # Expand dimensions for model input
    return img

# ✅ Classification Function
def classify_waste(img):
    img_array = preprocess_image(img)
    predictions = model.predict(img_array)

    # Debug: Print raw model output
    print("🔍 Raw model predictions:", predictions)

    predicted_index = np.argmax(predictions)
    predicted_class = CLASSES[predicted_index]

    # Debug: Show final predicted class
    print("✅ Predicted class:", predicted_class)

    return predicted_class

# ✅ Route to Handle Image Upload & Classification
@app.route("/classify", methods=["POST"])
def classify_image():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["image"]
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        print("❌ Error: Image could not be decoded.")
        return jsonify({"error": "Could not read image"}), 500

    print("✅ Image successfully read, shape:", img.shape)

    classification = classify_waste(img)

    return jsonify({"classification": classification})

# ✅ Run Flask Server
if __name__ == "__main__":
    app.run(debug=True)
