@echo off
echo ============================================
echo Starting Django Server with ML Model
echo ============================================
echo.

REM Check if model exists
if exist "proposed_model.joblib" (
    echo [OK] Model file found: proposed_model.joblib
) else (
    echo [WARNING] Model file NOT found!
    echo.
    echo Please run the last cell in your Jupyter notebook to save the model.
    echo The cell will save: proposed_model.joblib
    echo.
    echo The server will start but /api/predict/ will return an error.
    echo.
)

echo.
echo Starting server at http://127.0.0.1:8000/
echo.
echo Available endpoints:
echo   - http://127.0.0.1:8000/api/profiles/
echo   - http://127.0.0.1:8000/api/predict/  (ML predictions)
echo   - http://127.0.0.1:8000/admin/
echo.
echo Press CTRL+C to stop the server
echo ============================================
echo.

python manage.py runserver
