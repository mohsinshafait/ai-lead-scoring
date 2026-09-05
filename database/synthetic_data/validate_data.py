# Import the required library.
import pandas as pd


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

# Define the folder containing our generated datasets.
DATA_PATH = "database/synthetic_data/output/"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

# Load all generated datasets.
courses_df = pd.read_csv(DATA_PATH + "courses.csv")
learners_df = pd.read_csv(DATA_PATH + "learners.csv")
leads_df = pd.read_csv(DATA_PATH + "leads.csv")
interactions_df = pd.read_csv(DATA_PATH + "interactions.csv")
sales_actions_df = pd.read_csv(DATA_PATH + "sales_actions.csv")
outcomes_df = pd.read_csv(DATA_PATH + "outcomes.csv")


# --------------------------------------------------
# 1. BASIC DATASET INFORMATION
# --------------------------------------------------

print("\n" + "=" * 60)
print("BASIC DATASET INFORMATION")
print("=" * 60)

datasets = {
    "Courses": courses_df,
    "Learners": learners_df,
    "Leads": leads_df,
    "Interactions": interactions_df,
    "Sales Actions": sales_actions_df,
    "Outcomes": outcomes_df
}

# Display the number of rows and columns in each dataset.
for name, dataframe in datasets.items():
    print(
        f"{name}: "
        f"{dataframe.shape[0]} rows, "
        f"{dataframe.shape[1]} columns"
    )


# --------------------------------------------------
# 2. PRIMARY KEY VALIDATION
# --------------------------------------------------

print("\n" + "=" * 60)
print("PRIMARY KEY VALIDATION")
print("=" * 60)

# Define each dataset and its primary key.
primary_keys = {
    "Courses": (courses_df, "course_id"),
    "Learners": (learners_df, "learner_id"),
    "Leads": (leads_df, "lead_id"),
    "Interactions": (interactions_df, "interaction_id"),
    "Sales Actions": (sales_actions_df, "action_id"),
    "Outcomes": (outcomes_df, "outcome_id")
}

# Check whether each primary key is unique.
for name, (dataframe, primary_key) in primary_keys.items():

    duplicate_count = dataframe[primary_key].duplicated().sum()

    if duplicate_count == 0:
        print(f"PASS: {name} -> {primary_key} is unique")

    else:
        print(
            f"FAIL: {name} -> "
            f"{duplicate_count} duplicate IDs found"
        )


# --------------------------------------------------
# 3. FOREIGN KEY VALIDATION
# --------------------------------------------------

print("\n" + "=" * 60)
print("FOREIGN KEY VALIDATION")
print("=" * 60)

# Check that every learner referenced by a lead exists.
invalid_learner_ids = (
    ~leads_df["learner_id"]
    .isin(learners_df["learner_id"])
).sum()

print(
    "Leads -> Learners: "
    f"{invalid_learner_ids} invalid references"
)


# Check that every course referenced by a lead exists.
invalid_course_ids = (
    ~leads_df["course_id"]
    .isin(courses_df["course_id"])
).sum()

print(
    "Leads -> Courses: "
    f"{invalid_course_ids} invalid references"
)


# Check that every interaction belongs to a valid lead.
invalid_interaction_leads = (
    ~interactions_df["lead_id"]
    .isin(leads_df["lead_id"])
).sum()

print(
    "Interactions -> Leads: "
    f"{invalid_interaction_leads} invalid references"
)


# Check that every sales action belongs to a valid lead.
invalid_action_leads = (
    ~sales_actions_df["lead_id"]
    .isin(leads_df["lead_id"])
).sum()

print(
    "Sales Actions -> Leads: "
    f"{invalid_action_leads} invalid references"
)


# Check that every outcome belongs to a valid lead.
invalid_outcome_leads = (
    ~outcomes_df["lead_id"]
    .isin(leads_df["lead_id"])
).sum()

print(
    "Outcomes -> Leads: "
    f"{invalid_outcome_leads} invalid references"
)


# --------------------------------------------------
# 4. MISSING VALUE VALIDATION
# --------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

# Count missing values in every dataset.
for name, dataframe in datasets.items():

    missing_values = dataframe.isnull().sum().sum()

    print(
        f"{name}: "
        f"{missing_values} missing values"
    )

# --------------------------------------------------
# 4.1 BUSINESS-AWARE MISSING VALUE VALIDATION
# --------------------------------------------------

print("\n" + "=" * 60)
print("BUSINESS-AWARE MISSING VALUE VALIDATION")
print("=" * 60)


# --------------------------------------------------
# SALES ACTIONS
# --------------------------------------------------

# A completed action should have a completion date.
completed_without_date = (
    (sales_actions_df["action_status"] == "Completed")
    &
    (sales_actions_df["completed_at"].isnull())
).sum()

print(
    "Completed actions without completion date: "
    f"{completed_without_date}"
)


# A pending action should not have a completion date.
pending_with_date = (
    (sales_actions_df["action_status"] == "Pending")
    &
    (sales_actions_df["completed_at"].notnull())
).sum()

print(
    "Pending actions with completion date: "
    f"{pending_with_date}"
)


# --------------------------------------------------
# OUTCOMES
# --------------------------------------------------

# A converted lead should have a conversion date.
converted_without_date = (
    (outcomes_df["converted"] == 1)
    &
    (outcomes_df["conversion_date"].isnull())
).sum()

print(
    "Converted leads without conversion date: "
    f"{converted_without_date}"
)


# A non-converted lead should not have a conversion date.
non_converted_with_date = (
    (outcomes_df["converted"] == 0)
    &
    (outcomes_df["conversion_date"].notnull())
).sum()

print(
    "Non-converted leads with conversion date: "
    f"{non_converted_with_date}"
)

# --------------------------------------------------
# 5. COURSE AND LEARNER LEVEL VALIDATION
# --------------------------------------------------

print("\n" + "=" * 60)
print("COURSE-LEARNER MATCH VALIDATION")
print("=" * 60)

# Merge leads with learners to check learner levels.
lead_learner_df = leads_df.merge(
    learners_df[
        ["learner_id", "student_level"]
    ],
    on="learner_id",
    how="left"
)

# Merge the result with courses.
lead_course_df = lead_learner_df.merge(
    courses_df[
        ["course_id", "student_level"]
    ],
    on="course_id",
    how="left",
    suffixes=("_learner", "_course")
)

# Count leads where the learner level does not
# match the selected course level.
level_mismatches = (
    lead_course_df["student_level_learner"]
    != lead_course_df["student_level_course"]
).sum()

print(
    f"Course-level mismatches: "
    f"{level_mismatches}"
)


# --------------------------------------------------
# 6. DATE VALIDATION
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATE VALIDATION")
print("=" * 60)

# Convert date columns into datetime format.
leads_df["created_at"] = pd.to_datetime(
    leads_df["created_at"]
)

interactions_df["interaction_at"] = pd.to_datetime(
    interactions_df["interaction_at"]
)

sales_actions_df["created_at"] = pd.to_datetime(
    sales_actions_df["created_at"]
)

sales_actions_df["completed_at"] = pd.to_datetime(
    sales_actions_df["completed_at"]
)

outcomes_df["conversion_date"] = pd.to_datetime(
    outcomes_df["conversion_date"]
)


# Merge interaction dates with lead creation dates.
interaction_dates = interactions_df.merge(
    leads_df[["lead_id", "created_at"]],
    on="lead_id",
    how="left"
)

# Count interactions that occurred before the lead existed.
invalid_interaction_dates = (
    interaction_dates["interaction_at"]
    < interaction_dates["created_at"]
).sum()

print(
    "Interactions before lead creation: "
    f"{invalid_interaction_dates}"
)


# Merge outcome dates with lead creation dates.
outcome_dates = outcomes_df.merge(
    leads_df[["lead_id", "created_at"]],
    on="lead_id",
    how="left"
)

# Count conversions that happened before lead creation.
invalid_conversion_dates = (
    outcome_dates["conversion_date"]
    < outcome_dates["created_at"]
).sum()

print(
    "Conversions before lead creation: "
    f"{invalid_conversion_dates}"
)


# --------------------------------------------------
# 7. BUSINESS LOGIC VALIDATION
# --------------------------------------------------

print("\n" + "=" * 60)
print("BUSINESS LOGIC VALIDATION")
print("=" * 60)

# Check that converted leads generated revenue.
converted_without_revenue = (
    (
        outcomes_df["converted"] == 1
    )
    &
    (
        outcomes_df["revenue"] <= 0
    )
).sum()

print(
    "Converted leads without revenue: "
    f"{converted_without_revenue}"
)


# Check that non-converted leads generated no revenue.
non_converted_with_revenue = (
    (
        outcomes_df["converted"] == 0
    )
    &
    (
        outcomes_df["revenue"] > 0
    )
).sum()

print(
    "Non-converted leads with revenue: "
    f"{non_converted_with_revenue}"
)


# --------------------------------------------------
# 8. CONVERSION BY ENGAGEMENT
# --------------------------------------------------

print("\n" + "=" * 60)
print("CONVERSION BY ENGAGEMENT")
print("=" * 60)

# Count interactions for every lead.
interaction_counts = (
    interactions_df
    .groupby("lead_id")
    .size()
    .reset_index(name="interaction_count")
)

# Merge interaction counts with outcomes.
engagement_analysis = outcomes_df.merge(
    interaction_counts,
    on="lead_id",
    how="left"
)

# Replace missing interaction counts with zero.
engagement_analysis["interaction_count"] = (
    engagement_analysis["interaction_count"]
    .fillna(0)
)


# Create engagement groups.
engagement_analysis["engagement_group"] = pd.cut(
    engagement_analysis["interaction_count"],
    bins=[-1, 2, 5, float("inf")],
    labels=["Low", "Medium", "High"]
)

# Calculate the conversion rate for each group.
engagement_conversion = (
    engagement_analysis
    .groupby(
        "engagement_group",
        observed=False
    )["converted"]
    .mean()
    * 100
)

print(
    engagement_conversion
)


# --------------------------------------------------
# 9. OVERALL CONVERSION SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("OVERALL CONVERSION SUMMARY")
print("=" * 60)

# Calculate and display the overall conversion rate.
overall_conversion_rate = (
    outcomes_df["converted"].mean()
    * 100
)

print(
    f"Overall conversion rate: "
    f"{overall_conversion_rate:.2f}%"
)


# Display the number of converted and
# non-converted leads.
print(
    outcomes_df["converted"]
    .value_counts()
)


# --------------------------------------------------
# VALIDATION COMPLETE
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATA VALIDATION COMPLETED")
print("=" * 60)