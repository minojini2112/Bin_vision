from flask import Flask, request, jsonify
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
from flask_cors import CORS

app = Flask(__name__)  # ✅ Fixed typo
CORS(app)  # ✅ Move CORS after defining app

app.config["UPLOAD_FOLDER"] = "uploads/"

# ✅ Waste Categories
BIODEGRADABLE = ['cardboard', 'paper', 'trash']
NON_BIODEGRADABLE = ['glass', 'metal', 'plastic']
CLASSES = BIODEGRADABLE + NON_BIODEGRADABLE  # 6 classes

# ✅ Load Model
MODEL_PATH = "waste_classifier.h5"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found.")
model = load_model(MODEL_PATH)
print("✅ Model loaded successfully with 6 classes!")

# ✅ Image Preprocessing
def preprocess_image(img):
    img = cv2.resize(img, (224, 224))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# ✅ Classification Function
def classify_waste(img):
    img_array = preprocess_image(img)
    predictions = model.predict(img_array)
    return CLASSES[np.argmax(predictions)]

# ✅ Route to Handle Image Upload & Classification
@app.route("/classify", methods=["POST"])
def classify_image():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["image"]
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    # Ensure the upload directory exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    
    file.save(filepath)

    img = cv2.imread(filepath)
    if img is None:
        return jsonify({"error": "Could not read image"}), 500

    classification = classify_waste(img)

    return jsonify({"classification": classification})

if __name__ == "__main__":  # ✅ Fixed typo
    app.run(debug=True)
