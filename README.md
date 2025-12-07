# Health Prediction API

Django REST API for predicting health anomalies based on vital signs (Temperature, SpO2, BPM).

## Setup Instructions

### 1. Install Dependencies

```bash
python3 -m pip install django djangorestframework joblib scikit-learn numpy pandas imbalanced-learn
```

### 2. Train the Model

```bash
python3 train_model.py
```

This will:
- Load and clean the dataset from `data/Full Final.csv`
- Train an ensemble model (Random Forest + Gradient Boosting + Logistic Regression)
- Save the model as `proposed_model.joblib`

### 3. Run Django Server

```bash
cd app
python3 manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## API Usage

### Endpoint: POST /profile

**URL:** `http://127.0.0.1:8000/profile`

**Request Body (JSON):**
```json
{
  "Temp_C": 37.0,
  "SpO2": 99,
  "BPM": 70
}
```

**Response (JSON):**
```json
{
  "prediction": "Normal",
  "probability": 0.1234,
  "input_data": {
    "Temp_C": 37.0,
    "SpO2": 99,
    "BPM": 70
  }
}
```

### Example Using cURL

```bash
curl -X POST http://127.0.0.1:8000/profile \
  -H "Content-Type: application/json" \
  -d '{"Temp_C": 37.0, "SpO2": 99, "BPM": 70}'
```

### Example Using Python

```python
import requests

url = "http://127.0.0.1:8000/profile"
data = {
    "Temp_C": 37.0,
    "SpO2": 99,
    "BPM": 70
}

response = requests.post(url, json=data)
print(response.json())
```

## Project Structure

```
.
├── app/                    # Django project
│   ├── app/               # Main Django app
│   │   ├── settings.py    # Django settings
│   │   └── urls.py        # Main URL routing
│   ├── predictions/       # Predictions API app
│   │   ├── views.py       # API endpoint logic
│   │   └── urls.py        # API URL routing
│   ├── manage.py          # Django management script
│   └── db.sqlite3         # SQLite database
├── data/                  # Dataset folder
│   └── Full Final.csv     # Training data
├── model.ipynb            # Jupyter notebook for model exploration
├── train_model.py         # Script to train and save model
├── proposed_model.joblib  # Saved ML model (generated)
└── README.md              # This file
```

## Model Details

- **Algorithm:** Ensemble Voting Classifier
  - Random Forest (400 estimators)
  - Gradient Boosting (300 estimators, lr=0.05)
  - Logistic Regression (with StandardScaler)
- **Decision Threshold:** 0.45 (tuned for better recall)
- **Performance:** ~95% accuracy, ~99% ROC-AUC

## Notes

- The model expects 3 features: `Temp_C`, `SpO2`, `BPM`
- Missing any field will return a 400 Bad Request error
- Invalid data types will return a 400 Bad Request error
- If model file is not found, returns 500 Internal Server Error
