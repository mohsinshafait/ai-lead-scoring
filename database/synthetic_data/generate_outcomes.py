# Import the required libraries.
import pandas as pd
import random
import os
from datetime import timedelta


# Set a random seed so the generated data is reproducible.
random.seed(42)


# Define the input and output file paths.
LEADS_PATH = "database/synthetic_data/output/leads.csv"
COURSES_PATH = "database/synthetic_data/output/courses.csv"
INTERACTIONS_PATH = "database/synthetic_data/output/interactions.csv"
SALES_ACTIONS_PATH = "database/synthetic_data/output/sales_actions.csv"

OUTPUT_PATH = "database/synthetic_data/output/outcomes.csv"


# Load all previously generated datasets.
leads_df = pd.read_csv(LEADS_PATH)
courses_df = pd.read_csv(COURSES_PATH)
interactions_df = pd.read_csv(INTERACTIONS_PATH)
sales_actions_df = pd.read_csv(SALES_ACTIONS_PATH)


# Create an empty list to store outcome records.
outcomes = []


# Start outcome IDs from 1.
outcome_id = 1


# Define lead source conversion quality.
# Some lead sources generally show stronger intent than others.
lead_source_scores = {
    "Referral": 0.15,
    "Google Search": 0.10,
    "Website": 0.08,
    "WhatsApp": 0.08,
    "YouTube": 0.05,
    "Facebook": 0.03,
    "Instagram": 0.03
}


# Define a function to calculate the conversion probability.
def calculate_conversion_probability(
    lead,
    course_price,
    interaction_count,
    completed_actions
):
    """
    Calculate a realistic conversion probability
    using lead information, engagement behavior,
    budget fit, and completed sales actions.
    """

    # Start with a base conversion probability.
    probability = 0.10

    # ------------------------------------------------
    # 1. BUDGET FIT
    # ------------------------------------------------

    # Get the lead's available budget.
    budget = lead["budget"]

    # Calculate how well the budget matches the course price.
    budget_ratio = budget / course_price

    # A lead with enough budget has a higher chance of converting.
    if budget_ratio >= 1.0:
        probability += 0.20

    # A lead with a slightly lower budget may still convert.
    elif budget_ratio >= 0.80:
        probability += 0.10

    # A significantly lower budget reduces conversion probability.
    elif budget_ratio < 0.60:
        probability -= 0.08

    # ------------------------------------------------
    # 2. LEAD SOURCE
    # ------------------------------------------------

    # Add the conversion score based on the source.
    probability += lead_source_scores.get(
        lead["lead_source"],
        0
    )

    # ------------------------------------------------
    # 3. DECISION MAKER
    # ------------------------------------------------

    # If the learner is the decision-maker,
    # the decision process may be faster.
    if lead["decision_maker_type"] == "Learner":
        probability += 0.03

    # ------------------------------------------------
    # 4. ENGAGEMENT
    # ------------------------------------------------

    # More interactions usually indicate stronger interest.
    if interaction_count >= 6:
        probability += 0.20

    elif interaction_count >= 4:
        probability += 0.12

    elif interaction_count >= 2:
        probability += 0.05

    # ------------------------------------------------
    # 5. COMPLETED SALES ACTIONS
    # ------------------------------------------------

    # Completed follow-ups increase the probability of conversion.
    if completed_actions >= 3:
        probability += 0.15

    elif completed_actions >= 2:
        probability += 0.10

    elif completed_actions >= 1:
        probability += 0.05

    # ------------------------------------------------
    # 6. RANDOM REAL-WORLD VARIATION
    # ------------------------------------------------

    # Add some random variation because not every
    # business decision can be explained by our features.
    probability += random.uniform(-0.08, 0.08)

    # Keep the probability between 1% and 95%.
    probability = max(
        0.01,
        min(probability, 0.95)
    )

    # Return the final probability rounded to four decimals.
    return round(probability, 4)


# Loop through every lead.
for _, lead in leads_df.iterrows():

    # Get the current lead ID.
    lead_id = lead["lead_id"]

    # Find the course connected to this lead.
    course = courses_df[
        courses_df["course_id"] == lead["course_id"]
    ].iloc[0]

    # Get the price of the selected course.
    course_price = course["price"]

    # Count the number of interactions for this lead.
    interaction_count = len(
        interactions_df[
            interactions_df["lead_id"] == lead_id
        ]
    )

    # Find the completed sales actions for this lead.
    completed_actions = len(
        sales_actions_df[
            (sales_actions_df["lead_id"] == lead_id)
            &
            (sales_actions_df["action_status"] == "Completed")
        ]
    )

    # Calculate the conversion probability.
    conversion_probability = calculate_conversion_probability(
        lead,
        course_price,
        interaction_count,
        completed_actions
    )

    # Decide whether the lead converted.
    # The random number is compared with the calculated probability.
    converted = (
        random.random() < conversion_probability
    )

    # Convert the lead creation date into datetime format.
    lead_created_at = pd.to_datetime(
        lead["created_at"]
    )

    # Generate conversion information.
    if converted:

        # Generate a realistic conversion date.
        conversion_date = lead_created_at + timedelta(
            days=random.randint(1, 60)
        )

        # Define the final status.
        final_status = "Converted"

        # Revenue is based on the course price.
        revenue = course_price

    else:

        # Non-converted leads do not have a conversion date.
        conversion_date = None

        # Define the final status.
        final_status = "Not Converted"

        # No revenue is generated.
        revenue = 0

    # Create the outcome record.
    outcome = {
        "outcome_id": outcome_id,
        "lead_id": lead_id,
        "converted": int(converted),
        "conversion_probability": conversion_probability,
        "conversion_date": conversion_date,
        "final_status": final_status,
        "revenue": revenue
    }

    # Add the outcome to the list.
    outcomes.append(outcome)

    # Increase the outcome ID.
    outcome_id += 1


# Convert the outcome records into a DataFrame.
outcomes_df = pd.DataFrame(outcomes)


# Create the output directory if it does not exist.
os.makedirs(
    "database/synthetic_data/output",
    exist_ok=True
)


# Save the outcomes dataset.
outcomes_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# Display the first five outcome records.
print(outcomes_df.head())


# Display the total number of outcome records.
print(
    f"\nTotal outcomes generated: "
    f"{len(outcomes_df)}"
)


# Display the overall conversion rate.
conversion_rate = (
    outcomes_df["converted"].mean() * 100
)

print(
    f"Conversion rate: "
    f"{conversion_rate:.2f}%"
)


# Display the number of converted leads.
print(
    f"Converted leads: "
    f"{outcomes_df['converted'].sum()}"
)