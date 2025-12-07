# 🚀 Quick Start Guide: Access ML Model via Django API

## ✅ What's Already Done:
1. ✅ Django API created with profile endpoints
2. ✅ ML prediction endpoint created (`/api/predict/`)
3. ✅ Required packages installed (pandas, numpy, scikit-learn, joblib)
4. ✅ Code is ready to load and use your model

## 📋 What YOU Need to Do:

### Step 1: Save the Model from Jupyter Notebook
**Action:** Go to your Jupyter notebook (`my-data2(4).ipynb`) and run the **last cell** (cell 39)

This cell will save your trained `proposed_model` to:
```
d:\Django ApI\newproject\proposed_model.joblib
```

### Step 2: Restart Django Server
After saving the model, restart your server:

**Option A: Stop and Start**
- Press `CTRL+C` in the terminal running the server
- Run: `python manage.py runserver`

**Option B: Just reload** (server auto-reloads when it detects the model file)

## 🎯 How to Use the API:

### Test the Prediction Endpoint

**URL:** `POST http://127.0.0.1:8000/api/predict/`

**Example 1: Using Browser (REST Framework UI)**
1. Go to: `http://127.0.0.1:8000/api/predict/`
2. Scroll down to the form
3. Enter JSON:
```json
{
    "Temp_C": 37.5,
    "SpO2": 95,
    "BPM": 72
}
```
4. Click "POST"

**Example 2: Using PowerShell**
```powershell
$body = @{
    Temp_C = 38.5
    SpO2 = 92
    BPM = 85
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/predict/" -Method POST -Headers @{"Content-Type"="application/json"} -Body $body
```

**Example 3: Using Python**
```python
import requests

data = {
    "Temp_C": 37.5,
    "SpO2": 95,
    "BPM": 72
}

response = requests.post("http://127.0.0.1:8000/api/predict/", json=data)
print(response.json())
```

## 📤 Expected Response:
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

## 🔍 Troubleshooting:

**Problem:** "ML model not loaded" error
- **Solution:** Make sure you ran the notebook cell to save the model
- Check if file exists: `Test-Path "d:\Django ApI\newproject\proposed_model.joblib"`

**Problem:** ModuleNotFoundError
- **Solution:** Server was running before packages were installed
- Restart the server with `CTRL+C` then `python manage.py runserver`

**Problem:** Invalid input error
- **Solution:** Make sure you're sending all three required fields: `Temp_C`, `SpO2`, `BPM`
- All values must be numbers

## 📍 All Available Endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/profiles/` | GET | List all profiles |
| `/api/profiles/` | POST | Create new profile |
| `/api/predict/` | POST | **Predict anomaly from vitals** |
| `/admin/` | GET | Django admin panel |

## 🎓 Next Steps:
- Test different vital sign combinations
- Integrate the API into a frontend application
- Add authentication if needed
- Deploy to production server

Good luck! 🚀
