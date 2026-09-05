from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from src.data_loader import load_initial_dataset


# --------------------------------
# 1. Load data
# --------------------------------

df = load_initial_dataset()

print("Dataset shape:", df.shape)


# --------------------------------
# 2. Separate features and target
# --------------------------------

X = df.drop(columns=["converted", "lead_id"])
y = df["converted"]


# --------------------------------
# 3. Define feature types
# --------------------------------

numerical_features = [
    "budget",
    "age_at_lead",
    "duration_weeks",
    "price",
    "budget_price_ratio",
    "budget_gap"
]

categorical_features = [
    "lead_source",
    "campaign",
    "lead_type",
    "decision_maker_type",
    "preferred_contact_method",
    "learner_student_level",
    "city",
    "country",
    "course_name",
    "course_student_level",
    "subject",
    "delivery_mode"
]


# --------------------------------
# 4. Train/Test Split
# --------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training samples:", X_train.shape)
print("Testing samples:", X_test.shape)


# --------------------------------
# 5. Numerical preprocessing
# --------------------------------

numerical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])


# --------------------------------
# 6. Categorical preprocessing
# --------------------------------

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    (
        "encoder",
        OneHotEncoder(
            handle_unknown="ignore",
            sparse_output=False
        )
    )
])


# --------------------------------
# 7. Combine preprocessing
# --------------------------------

preprocessor = ColumnTransformer([
    ("num", numerical_pipeline, numerical_features),
    ("cat", categorical_pipeline, categorical_features)
])


# --------------------------------
# 8. Define models
# --------------------------------

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingClassifier(
        random_state=42
    )
}


# --------------------------------
# 9. Train and evaluate models
# --------------------------------

trained_models = {}

for name, classifier in models.items():

    print(f"\nTraining {name}...")

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", classifier)
    ])

    pipeline.fit(X_train, y_train)

    trained_models[name] = pipeline

    # Predictions
    y_pred = pipeline.predict(X_test)

    # Conversion probability
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")


import joblib
from pathlib import Path

model_path = Path("models/initial")
model_path.mkdir(parents=True, exist_ok=True)

joblib.dump(
    pipeline,
    model_path / "initial_lead_scoring_model.pkl"
)

print("\nInitial model saved successfully.")
print(
    f"Path: {model_path / 'initial_lead_scoring_model.pkl'}"
)