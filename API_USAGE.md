# ML Model API Integration Guide

## Setup Instructions

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Copy Your Trained Model
Copy the `proposed_model.joblib` file from your Jupyter notebook directory to the Django project root:
```powershell
# The model should be at: d:\Django ApI\newproject\proposed_model.joblib
```

### 3. Run the Server
```powershell
python manage.py runserver
```

## API Endpoints

### 🔮 Predict Anomaly (ML Model)
**Endpoint:** `POST http://127.0.0.1:8000/api/predict/`

**Request Body:**
```json
{
    "Temp_C": 37.5,
    "SpO2": 95,
    "BPM": 72
}
```

**Response:**
```json
{
    "input": {
        "Temp_C": 37.5,
        "SpO2": 95,
        "BPM": 72
    },
    "prediction": "Normal",
    "prediction_code": 0,
    "abnormal_probability": 0.1234,
    "normal_probability": 0.8766,
    "threshold_used": 0.45,
    "recommendation": "Vitals appear normal"
}
```

**PowerShell Test Command:**
```powershell
$body = @{
    Temp_C = 37.5
    SpO2 = 95
    BPM = 72
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/predict/" -Method POST -Headers @{"Content-Type"="application/json"} -Body $body
```

### 👤 Profile Endpoints
**Create Profile:** `POST http://127.0.0.1:8000/api/profiles/`
**List Profiles:** `GET http://127.0.0.1:8000/api/profiles/`

## Notes
- The model uses the same threshold (0.45) as defined in your notebook
- Ensure `proposed_model.joblib` is in the project root directory
- The API expects features: `Temp_C`, `SpO2`, `BPM` (same as your trained model)
