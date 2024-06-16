from flask import Flask, request, jsonify, render_template, send_from_directory
import torch
import torchvision.transforms as transforms
import torchvision.models as models 
import torch.nn as nn
from PIL import Image
import io
import os
import base64
import uuid
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load the model
model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, 2)   # Assuming your model has 2 output classes
model.load_state_dict(torch.load(r'model/Cat_Dog_Classifier_StateDict.pth', map_location=torch.device('cpu')))
model.eval()

# Define image transformations
data_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the image from the request
        request_data = request.get_json()
        base64_image = request_data["image"]
        image_byte = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_byte))

        # Preprocess the image
        input_tensor = data_transform(image)
        input_batch = input_tensor.unsqueeze(0)  # Add a batch dimension

        # Make prediction
        with torch.no_grad():
            output = model(input_batch)
            _, predicted = torch.max(output, 1)
            class_index = predicted.item()

        # Return the classification result
        class_names = ['cat', 'dog']
        result = {'class': class_names[class_index]}

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
