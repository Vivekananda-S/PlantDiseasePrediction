from google.cloud import storage
import tensorflow as tf
from PIL import Image
import numpy as np

from flask import Flask, jsonify, request

BUCKET_NAME = "disease-classification" 
class_names = ['Pepper__bell___Bacterial_spot',
'Pepper__bell___healthy',
'Potato___Early_blight',
 'Potato___Late_blight',
 'Potato___healthy',
 'Tomato_Bacterial_spot',
 'Tomato_Early_blight',
 'Tomato_Late_blight',
 'Tomato_Leaf_Mold',
 'Tomato_Septoria_leaf_spot',
 'Tomato_Spider_mites_Two_spotted_spider_mite',
 'Tomato__Target_Spot',
 'Tomato__Tomato_YellowLeaf__Curl_Virus',
 'Tomato__Tomato_mosaic_virus',
 'Tomato_healthy']


model = None

def download_blob(bucket_name, soucre_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(soucre_blob_name)
    blob.download_to_filename(destination_file_name)

app = Flask(__name__)

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict(request):
    global model
    if model is None:
        download_blob(
            BUCKET_NAME,
            "models/model1.h5",
            "/tmp/model1.h5",
        )
        model = tf.keras.models.load_model("/tmp/model1.h5",compile=False)
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Success'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        return response

    image = request.files["file"]

    image = np.array(Image.open(image).convert("RGB").resize((224,224)))
    image = image/225
    img_array = tf.expand_dims(image, 0)

    predictions = model.predict(img_array)
    print(predictions)

    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0])), 2)

    response = jsonify({"class": predicted_class, "confidence": confidence})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)