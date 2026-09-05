from src.data_loader import load_dynamic_dataset
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


# ============================================================
# 1. LOAD DATA
# ============================================================

df = load_dynamic_dataset()

print("Dataset shape:", df.shape)


# ============================================================
# 2. DEFINE FEATURES
# ============================================================

numerical_features = [
    "budget",
    "age_at_lead",
    "duration_weeks",
    "price",
    "budget_price_ratio",
    "budget_gap",

    "total_interactions",
    "website_visits",
    "course_page_views",
    "pricing_page_views",
    "trial_class_requests",
    "email_inquiries",

    "total_sales_actions",
    "phone_calls",
    "whatsapp_followups",
    "email_followups",
    "trial_class_invitations",
    "free_consultations",
    "course_information_sent",
    "completed_sales_actions",
    "pending_sales_actions",
    "high_priority_actions",
    "medium_priority_actions",
    "low_priority_actions",
    "days_since_last_interaction",
    "days_since_last_sales_action",
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
    "delivery_mode",
]


# ============================================================
# 3. FEATURES + TARGET
# ============================================================

feature_columns = numerical_features + categorical_features

X = df[feature_columns]
y = df["converted"]


# ============================================================
# 4. SPLIT BY LEAD
# ============================================================

unique_leads = df["lead_id"].unique()

train_leads, test_leads = train_test_split(
    unique_leads,
    test_size=0.20,
    random_state=42
)

train_df = df[df["lead_id"].isin(train_leads)].copy()
test_df = df[df["lead_id"].isin(test_leads)].copy()


X_train = train_df[feature_columns]
y_train = train_df["converted"]

X_test = test_df[feature_columns]
y_test = test_df["converted"]


print("\nTraining shape:", X_train.shape)
print("Testing shape:", X_test.shape)

print("\nUnique training leads:", train_df["lead_id"].nunique())
print("Unique testing leads:", test_df["lead_id"].nunique())


# ============================================================
# 5. PREPROCESSING
# ============================================================

numerical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]
)


categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        )
    ]
)


preprocessor = ColumnTransformer(
    transformers=[
        ("num", numerical_pipeline, numerical_features),
        ("cat", categorical_pipeline, categorical_features),
    ]
)


# ============================================================
# 6. MODEL
# ============================================================

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)


pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ============================================================
# 7. TRAIN
# ============================================================

print("\nTraining Model 2...")

pipeline.fit(X_train, y_train)

print("Training completed.")


# ============================================================
# 8. OVERALL TEST PERFORMANCE
# ============================================================

y_pred = pipeline.predict(X_test)
y_probability = pipeline.predict_proba(X_test)[:, 1]


print("\n==============================")
print("OVERALL MODEL 2 PERFORMANCE")
print("==============================")


print(
    "Accuracy:",
    round(accuracy_score(y_test, y_pred), 4)
)

print(
    "Precision:",
    round(precision_score(y_test, y_pred), 4)
)

print(
    "Recall:",
    round(recall_score(y_test, y_pred), 4)
)

print(
    "F1 Score:",
    round(f1_score(y_test, y_pred), 4)
)

print(
    "ROC-AUC:",
    round(roc_auc_score(y_test, y_probability), 4)
)


# ============================================================
# 9. PERFORMANCE BY SNAPSHOT
# ============================================================

print("\n==============================")
print("PERFORMANCE BY SNAPSHOT")
print("==============================")


for day in [0, 3, 7, 14]:

    snapshot_test = test_df[
        test_df["snapshot_day"] == day
    ]

    X_snapshot = snapshot_test[feature_columns]
    y_snapshot = snapshot_test["converted"]

    predictions = pipeline.predict(X_snapshot)

    probabilities = pipeline.predict_proba(
        X_snapshot
    )[:, 1]

    print(f"\nDay {day}")

    print(
        "Samples:",
        len(snapshot_test)
    )

    print(
        "Accuracy:",
        round(
            accuracy_score(
                y_snapshot,
                predictions
            ),
            4
        )
    )

    print(
        "Precision:",
        round(
            precision_score(
                y_snapshot,
                predictions
            ),
            4
        )
    )

    print(
        "Recall:",
        round(
            recall_score(
                y_snapshot,
                predictions
            ),
            4
        )
    )

    print(
        "F1:",
        round(
            f1_score(
                y_snapshot,
                predictions
            ),
            4
        )
    )

    print(
        "ROC-AUC:",
        round(
            roc_auc_score(
                y_snapshot,
                probabilities
            ),
            4
        )
    )

# ============================================================
# 10. FEATURE IMPORTANCE
# ============================================================

feature_names = pipeline.named_steps[
    "preprocessor"
].get_feature_names_out()

coefficients = pipeline.named_steps[
    "model"
].coef_[0]

feature_importance = (
    pd.DataFrame({
        "feature": feature_names,
        "coefficient": coefficients
    })
    .sort_values(
        "coefficient",
        ascending=False
    )
)

print("\n==============================")
print("TOP POSITIVE FEATURES")
print("==============================")

print(
    feature_importance.head(15).to_string(index=False)
)


print("\n==============================")
print("TOP NEGATIVE FEATURES")
print("==============================")

print(
    feature_importance.tail(15)
    .sort_values("coefficient")
    .to_string(index=False)
)


# ============================================================
# 11. SCORE TRAJECTORIES
# ============================================================

test_scores = pipeline.predict_proba(X_test)[:, 1]

test_results = test_df[["lead_id", "snapshot_day", "converted"]].copy()
test_results["conversion_probability"] = test_scores

test_results = test_results.sort_values(
    ["lead_id", "snapshot_day"]
)

print("\n==============================")
print("SAMPLE LEAD SCORE TRAJECTORIES")
print("==============================")

sample_leads = (
    test_results["lead_id"]
    .drop_duplicates()
    .head(10)
)

for lead_id in sample_leads:

    lead_history = test_results[
        test_results["lead_id"] == lead_id
    ][
        ["snapshot_day", "conversion_probability", "converted"]
    ]

    print(f"\nLead {lead_id}")
    print(
        lead_history.to_string(index=False)
    )

# ============================================================
# 12. SCORE MOVEMENT ANALYSIS
# ============================================================

trajectory = (
    test_results
    .pivot(
        index="lead_id",
        columns="snapshot_day",
        values="conversion_probability"
    )
    .reset_index()
)

# Calculate score changes
trajectory["change_0_to_3"] = (
    trajectory[3] - trajectory[0]
)

trajectory["change_3_to_7"] = (
    trajectory[7] - trajectory[3]
)

trajectory["change_7_to_14"] = (
    trajectory[14] - trajectory[7]
)

trajectory["change_0_to_14"] = (
    trajectory[14] - trajectory[0]
)

print("\n==============================")
print("SCORE MOVEMENT ANALYSIS")
print("==============================")

print(
    trajectory[
        [
            "lead_id",
            "change_0_to_3",
            "change_3_to_7",
            "change_7_to_14",
            "change_0_to_14"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 13. OVERALL SCORE MOVEMENT
# ============================================================

movement = trajectory["change_0_to_14"].dropna()

print("\n==============================")
print("OVERALL SCORE MOVEMENT")
print("==============================")

print(
    f"Leads with Day 0 and Day 14: {len(movement)}"
)

print(
    f"Average change: {movement.mean():.4f}"
)

print(
    f"Median change: {movement.median():.4f}"
)

print(
    f"Score increased: {(movement > 0.05).sum()}"
)

print(
    f"Score decreased: {(movement < -0.05).sum()}"
)

print(
    f"Score relatively stable: "
    f"{((movement >= -0.05) & (movement <= 0.05)).sum()}"
)


# ============================================================
# 14. SAVE DYNAMIC MODEL
# ============================================================

import joblib
from pathlib import Path

model_path = Path("models/dynamic")
model_path.mkdir(parents=True, exist_ok=True)

joblib.dump(
    pipeline,
    model_path / "dynamic_lead_scoring_model.pkl"
)

print("\nDynamic model saved successfully.")
print(
    f"Path: {model_path / 'dynamic_lead_scoring_model.pkl'}"
)