"""
Train and save the ML model for health prediction
"""
import numpy as np
import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore")

# Load dataset
print("Loading dataset...")
data_path = "data/Full Final.csv"
df = pd.read_csv(data_path)

# Keep relevant columns
df = df[["Temp_C", "Temp_F", "SpO2", "BPM", "Anomaly"]]

# Data cleaning
print("Cleaning data...")
df["Temp_C"] = pd.to_numeric(df["Temp_C"].astype(str).str.replace(r"[^0-9\.\+\-]", "", regex=True), errors="coerce")
df["Temp_F"] = pd.to_numeric(df["Temp_F"].astype(str).str.replace(r"[^0-9\.\+\-]", "", regex=True), errors="coerce")
df["SpO2"] = pd.to_numeric(df["SpO2"], errors="coerce")
df["BPM"] = pd.to_numeric(df["BPM"], errors="coerce")

# Drop duplicates
df.drop_duplicates(inplace=True)

# Handle SpO2 outliers
df.loc[df["SpO2"] > 100, "SpO2"] = 100.0
df = df[~((df["SpO2"] < 50) & (~df["SpO2"].isna()))]

# Fill missing values
for col in ["SpO2", "BPM"]:
    class_medians = df.groupby("Anomaly")[col].transform("median")
    df[col] = df[col].fillna(class_medians)
    df[col].fillna(df[col].median(), inplace=True)

# Drop Temp_F (using only Temp_C)
df = df.drop(columns=["Temp_F"])

# Encode labels
label_mapping = {"Normal": 0, "Abnormal": 1}
df["Anomaly_Code"] = df["Anomaly"].map(label_mapping)

# Features and target
feature_cols = ["Temp_C", "SpO2", "BPM"]
X = df[feature_cols]
y = df["Anomaly_Code"]

# Train-test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# SMOTE
from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

print(f"Training set: {X_train_res.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# Train models
print("Training ensemble model...")
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Tuned Random Forest
best_rf = RandomForestClassifier(
    n_estimators=400,
    max_depth=None,
    min_samples_leaf=1,
    random_state=42
)

# Tuned Gradient Boosting
best_gb = GradientBoostingClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    random_state=42
)

# Logistic Regression with scaling
log_model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(class_weight="balanced", max_iter=1000))
])

# Ensemble model
proposed_model = VotingClassifier(
    estimators=[
        ("rf", best_rf),
        ("gb", best_gb),
        ("lr", log_model)
    ],
    voting="soft"
)

proposed_model.fit(X_train_res, y_train_res)

# Evaluate
print("\nEvaluating model...")
from sklearn.metrics import classification_report, roc_auc_score

y_pred = proposed_model.predict(X_test)
y_proba = proposed_model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred, target_names=["Normal", "Abnormal"]))
print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")

# Save model
model_path = "proposed_model.joblib"
joblib.dump(proposed_model, model_path)
print(f"\n✅ Model saved to: {model_path}")

# Test prediction
test_sample = pd.DataFrame(
    [[37.0, 99, 70]],
    columns=["Temp_C", "SpO2", "BPM"]
)
test_proba = proposed_model.predict_proba(test_sample)[0, 1]
test_pred = "Abnormal" if test_proba >= 0.45 else "Normal"
print(f"\nTest prediction: {test_pred} (probability: {test_proba:.4f})")
