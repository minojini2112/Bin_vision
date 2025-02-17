import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# ✅ Step 1: Set New Dataset Path
DATASET_PATH = r"C:\Users\Shapna\Bin_vision\TEST"  # Update with the correct dataset path

# ✅ Step 2: Verify Folder Structure
if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"🚨 Dataset folder not found at {DATASET_PATH}. Check extraction path.")

print("✅ Dataset directory exists.")
print("Checking dataset structure...")
categories = os.listdir(DATASET_PATH)

if len(categories) != 2:
    raise ValueError(f"🚨 Expected 2 categories (bio, non-bio), but found {len(categories)}.")

for category in categories:
    category_path = os.path.join(DATASET_PATH, category)
    if os.path.isdir(category_path):
        num_images = len(os.listdir(category_path))
        print(f"🔍 Checking {category}... {num_images} images found.")
        if num_images == 0:
            raise ValueError(f"🚨 No images found in {category}! Check dataset.")

# ✅ Step 3: Load Pretrained MobileNetV2
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Freeze pretrained layers

# ✅ Step 4: Add Custom Layers
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(128, activation='relu'),
    Dropout(0.3),  # Prevent overfitting
    Dense(2, activation='softmax')  # ✅ 2 Classes: Bio, Non-Bio
])

# ✅ Step 5: Compile the Model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# ✅ Step 6: Prepare Data with ImageDataGenerator
train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

val_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# ✅ Step 7: Train the Model
model.fit(train_generator, validation_data=val_generator, epochs=10)

# ✅ Step 8: Save the Model
model.save('waste_classifier.h5')
print("🎉 Model trained and saved as 'waste_classifier.h5'!")
