# Patient Management API

A Flask application that manages patient information with MongoDB integration.

## Prerequisites

- Python 3.8 or higher
- MongoDB installed and running locally
- pip (Python package manager)

## Setup

1. Clone this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Make sure MongoDB is running on your local machine
5. Configure your MongoDB connection in the `.env` file if needed

## Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## API Endpoints

- `GET /`: Welcome message
- `GET /api/patients`: Get all patients
- `GET /api/patients/<email>`: Get a specific patient by email
- `POST /api/patients`: Create a new patient
- `PUT /api/patients/<email>`: Update a patient by email
- `DELETE /api/patients/<email>`: Delete a patient by email

## Data Schema

```json
{
    "user": {
        "email": "string",
        "password": "string"
    },
    "contact": {
        "name": "string",
        "age": "string",
        "number": "string",
        "email": "string"
    },
    "medical": {
        "bloodtype": "string",
        "height": "string",
        "weight": "string",
        "lastcheckup": "string",
        "conditions": ["string"],
        "medications": ["string"],
        "diet": ["string"]
    },
    "emergency": {
        "name": "string",
        "phone": "string"
    }
}
```

## Example Usage

Create a new patient:
```bash
curl -X POST http://localhost:5000/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "user": {
        "email": "patient@example.com",
        "password": "securepassword123"
    },
    "contact": {
        "name": "John Doe",
        "age": "30",
        "number": "1234567890",
        "email": "john.doe@example.com"
    },
    "medical": {
        "bloodtype": "O+",
        "height": "180",
        "weight": "75",
        "lastcheckup": "2024-03-15",
        "conditions": ["Asthma", "Hypertension"],
        "medications": ["Albuterol", "Lisinopril"],
        "diet": ["Low Sodium", "High Protein"]
    },
    "emergency": {
        "name": "Jane Doe",
        "phone": "9876543210"
    }
}'
```

Get all patients:
```bash
curl http://localhost:5000/api/patients
```

Get a specific patient by email:
```bash
curl http://localhost:5000/api/patients/patient@example.com
```

Update a patient by email:
```bash
curl -X PUT http://localhost:5000/api/patients/patient@example.com \
  -H "Content-Type: application/json" \
  -d '{
    "medical": {
        "conditions": ["Asthma", "Hypertension", "Diabetes"],
        "medications": ["Albuterol", "Lisinopril", "Metformin"]
    }
}'
```

Delete a patient by email:
```bash
curl -X DELETE http://localhost:5000/api/patients/patient@example.com
``` 