from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
import joblib
import pandas as pd
import os
from django.conf import settings

# Create your views here.

# Load the ML model once when the module loads
MODEL_PATH = os.path.join(settings.BASE_DIR, 'proposed_model.joblib')
try:
    ml_model = joblib.load(MODEL_PATH)
    MODEL_LOADED = True
except FileNotFoundError:
    ml_model = None
    MODEL_LOADED = False
    print(f"Warning: Model file not found at {MODEL_PATH}")

DECISION_THRESHOLD = 0.45  # Same threshold used in training

@api_view(['POST', 'GET'])
def profile_list(request):
    """
    Create a new profile (POST) or list all profiles (GET)
    """
    if request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def predict_anomaly(request):
    """
    Predict anomaly based on vitals (Temp_C, SpO2, BPM)
    
    Expected input:
    {
        "Temp_C": 37.5,
        "SpO2": 95,
        "BPM": 72
    }
    """
    if not MODEL_LOADED:
        return Response(
            {"error": "ML model not loaded. Please ensure 'proposed_model.joblib' is in the project root."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    # Extract input data
    try:
        temp_c = float(request.data.get('Temp_C'))
        spo2 = float(request.data.get('SpO2'))
        bpm = float(request.data.get('BPM'))
    except (TypeError, ValueError):
        return Response(
            {"error": "Invalid input. Please provide numeric values for Temp_C, SpO2, and BPM."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create DataFrame for prediction (model expects these exact column names)
    input_data = pd.DataFrame(
        [[temp_c, spo2, bpm]],
        columns=['Temp_C', 'SpO2', 'BPM']
    )
    
    # Make prediction
    try:
        # Get probability
        proba = ml_model.predict_proba(input_data)[0, 1]
        
        # Apply custom threshold
        prediction = 1 if proba >= DECISION_THRESHOLD else 0
        prediction_label = "Abnormal" if prediction == 1 else "Normal"
        
        # Return detailed response
        response_data = {
            "input": {
                "Temp_C": temp_c,
                "SpO2": spo2,
                "BPM": bpm
            },
            "prediction": prediction_label,
            "prediction_code": prediction,
            "abnormal_probability": round(proba, 4),
            "normal_probability": round(1 - proba, 4),
            "threshold_used": DECISION_THRESHOLD,
            "recommendation": "Seek medical attention immediately" if prediction == 1 else "Vitals appear normal"
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"Prediction failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
