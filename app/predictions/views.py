from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import joblib
import pandas as pd
import os
from pathlib import Path

class ProfileView(APIView):
    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # Add CORS headers manually
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept"
        return response
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load model once during initialization
        base_dir = Path(__file__).resolve().parent.parent.parent
        model_path = base_dir / 'proposed_model.joblib'

        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            self.threshold = 0.45  # Same threshold from notebook
        else:
            self.model = None

    def options(self, request, *args, **kwargs):
        """
        Handle preflight OPTIONS request for CORS
        """
        response = Response()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept"
        return response

    def post(self, request):
        """
        POST endpoint to predict health anomaly
        Expected input: {"Temp_C": float, "SpO2": float, "BPM": float}
        Returns: {"prediction": "Normal" or "Abnormal", "probability": float}
        """
        try:
            # Check if model is loaded
            if self.model is None:
                return Response(
                    {"error": "Model not found. Please train and save the model first."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Get data from request
            data = request.data

            # Validate required fields
            required_fields = ['Temp_C', 'SpO2', 'BPM']
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                return Response(
                    {"error": f"Missing required fields: {', '.join(missing_fields)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create DataFrame with the input data
            input_df = pd.DataFrame(
                [[float(data['Temp_C']), float(data['SpO2']), float(data['BPM'])]],
                columns=['Temp_C', 'SpO2', 'BPM']
            )

            # Make prediction
            probability = self.model.predict_proba(input_df)[0, 1]
            prediction = 1 if probability >= self.threshold else 0
            prediction_label = "Abnormal" if prediction == 1 else "Normal"

            return Response({
                "prediction": prediction_label,
                "probability": round(float(probability), 4),
                "input_data": {
                    "Temp_C": float(data['Temp_C']),
                    "SpO2": float(data['SpO2']),
                    "BPM": float(data['BPM'])
                }
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {"error": f"Invalid data type: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Prediction failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
