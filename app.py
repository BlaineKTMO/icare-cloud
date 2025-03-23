from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://admin:password123@192.168.1.3:27017/icare?authSource=admin"
mongo = PyMongo(app)

# Helper function to convert ObjectId to string
def serialize_doc(doc):
    if doc is None:
        return None
    doc['_id'] = str(doc['_id'])
    return doc

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Patient Management API"})

# Create a new patient
@app.route('/api/patients', methods=['POST'])
def create_patient():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Validate required fields
    required_fields = ['user', 'contact', 'medical', 'emergency']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Check if patient with email already exists
    email = str(data['user']['email'])
    existing_patient = mongo.db.patients.find_one({"user.email": email})
    if existing_patient:
        return jsonify({"error": "Patient with this email already exists"}), 409
    
    # Ensure all fields are strings or arrays of strings
    try:
        patient_data = {
            'user': {
                'email': email,
                'password': str(data['user']['password'])
            },
            'contact': {
                'name': str(data['contact']['name']),
                'age': str(data['contact']['age']),
                'number': str(data['contact']['number']),
                'email': str(data['contact']['email'])
            },
            'medical': {
                'bloodtype': str(data['medical']['bloodtype']),
                'height': str(data['medical']['height']),
                'weight': str(data['medical']['weight']),
                'lastcheckup': str(data['medical']['lastcheckup']),
                'conditions': [str(condition) for condition in data['medical']['conditions']],
                'medications': [str(medication) for medication in data['medical']['medications']],
                'diet': [str(item) for item in data['medical']['diet']]
            },
            'emergency': {
                'name': str(data['emergency']['name']),
                'phone': str(data['emergency']['phone'])
            }
        }
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid data format"}), 400
    
    result = mongo.db.patients.insert_one(patient_data)
    return jsonify({
        "message": "Patient created successfully",
        "email": email
    }), 201

# Get all patients
@app.route('/api/patients', methods=['GET'])
def get_patients():
    patients = list(mongo.db.patients.find())
    return jsonify([serialize_doc(patient) for patient in patients])

# Get a single patient by email
@app.route('/api/patients/<email>', methods=['GET'])
def get_patient(email):
    try:
        patient = mongo.db.patients.find_one({"user.email": email})
        if patient:
            return jsonify(serialize_doc(patient))
        return jsonify({"error": "Patient not found"}), 404
    except:
        return jsonify({"error": "Invalid email format"}), 400

# Update a patient
@app.route('/api/patients/<email>', methods=['PUT'])
def update_patient(email):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        # Convert all fields to strings or arrays of strings
        update_data = {}
        if 'user' in data:
            update_data['user'] = {
                'email': str(data['user']['email']),
                'password': str(data['user']['password'])
            }
        if 'contact' in data:
            update_data['contact'] = {
                'name': str(data['contact']['name']),
                'age': str(data['contact']['age']),
                'number': str(data['contact']['number']),
                'email': str(data['contact']['email'])
            }
        if 'medical' in data:
            update_data['medical'] = {
                'bloodtype': str(data['medical']['bloodtype']),
                'height': str(data['medical']['height']),
                'weight': str(data['medical']['weight']),
                'lastcheckup': str(data['medical']['lastcheckup']),
                'conditions': [str(condition) for condition in data['medical']['conditions']],
                'medications': [str(medication) for medication in data['medical']['medications']],
                'diet': [str(item) for item in data['medical']['diet']]
            }
        if 'emergency' in data:
            update_data['emergency'] = {
                'name': str(data['emergency']['name']),
                'phone': str(data['emergency']['phone'])
            }

        result = mongo.db.patients.update_one(
            {"user.email": email},
            {"$set": update_data}
        )
        if result.modified_count:
            return jsonify({"message": "Patient updated successfully"})
        return jsonify({"error": "Patient not found"}), 404
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid data format"}), 400
    except:
        return jsonify({"error": "Invalid email format"}), 400

# Delete a patient
@app.route('/api/patients/<email>', methods=['DELETE'])
def delete_patient(email):
    try:
        result = mongo.db.patients.delete_one({"user.email": email})
        if result.deleted_count:
            return jsonify({"message": "Patient deleted successfully"})
        return jsonify({"error": "Patient not found"}), 404
    except:
        return jsonify({"error": "Invalid email format"}), 400

if __name__ == '__main__':
    app.run(debug=True) 