# Import the required libraries.
import pandas as pd
import random
import os
from datetime import timedelta


# Set a random seed so the generated data is reproducible.
random.seed(42)


# Define input and output file paths.
LEADS_PATH = "database/synthetic_data/output/leads.csv"
INTERACTIONS_PATH = "database/synthetic_data/output/interactions.csv"
OUTPUT_PATH = "database/synthetic_data/output/sales_actions.csv"


# Load the leads and interactions datasets.
leads_df = pd.read_csv(LEADS_PATH)
interactions_df = pd.read_csv(INTERACTIONS_PATH)


# Create an empty list to store sales action records.
sales_actions = []


# Start action IDs from 1.
action_id = 1


# Define possible action types.
action_types = [
    "Phone Call",
    "WhatsApp Follow-up",
    "Email Follow-up",
    "Free Consultation",
    "Trial Class Invitation",
    "Course Information Sent"
]


# Define a function to determine the number of
# interactions associated with a lead.
def get_interaction_count(lead_id):
    """
    Count how many interactions were generated
    for a specific lead.
    """

    return len(
        interactions_df[
            interactions_df["lead_id"] == lead_id
        ]
    )


# Define a function to generate sales actions.
def generate_actions(interaction_count):
    """
    Generate business actions based on the
    engagement level of the lead.
    """

    # Highly engaged leads usually receive
    # more direct and higher-priority actions.
    if interaction_count >= 5:

        number_of_actions = random.randint(2, 4)

        possible_actions = [
            "Phone Call",
            "WhatsApp Follow-up",
            "Free Consultation",
            "Trial Class Invitation"
        ]

        priority = "High"

    # Moderately engaged leads receive
    # standard follow-up actions.
    elif interaction_count >= 3:

        number_of_actions = random.randint(1, 3)

        possible_actions = [
            "WhatsApp Follow-up",
            "Email Follow-up",
            "Course Information Sent",
            "Phone Call"
        ]

        priority = "Medium"

    # Low-engagement leads receive
    # fewer and lower-cost follow-ups.
    else:

        number_of_actions = 1

        possible_actions = [
            "Email Follow-up",
            "Course Information Sent"
        ]

        priority = "Low"

    # Randomly select the required actions.
    selected_actions = random.sample(
        possible_actions,
        k=min(number_of_actions, len(possible_actions))
    )

    return selected_actions, priority


# Loop through every lead.
for _, lead in leads_df.iterrows():

    # Get the ID of the current lead.
    lead_id = lead["lead_id"]

    # Count the lead's interactions.
    interaction_count = get_interaction_count(
        lead_id
    )

    # Generate actions and their priority.
    selected_actions, priority = generate_actions(
        interaction_count
    )

    # Convert the lead creation time into datetime format.
    lead_created_at = pd.to_datetime(
        lead["created_at"]
    )

    # Create one record for each sales action.
    for action_type in selected_actions:

        # Generate the action after the lead was created.
        action_created_at = lead_created_at + timedelta(
            days=random.randint(0, 14),
            hours=random.randint(0, 23)
        )

        # Decide whether the action was completed.
        is_completed = random.choices(
            [True, False],
            weights=[0.75, 0.25]
        )[0]

        # Create the sales action record.
        action = {
            "action_id": action_id,
            "lead_id": lead_id,
            "action_type": action_type,
            "priority": priority,
            "action_status": (
                "Completed"
                if is_completed
                else "Pending"
            ),
            "action_details": (
                f"Synthetic {priority.lower()} priority "
                f"sales follow-up"
            ),
            "created_at": action_created_at,
            "completed_at": (
                action_created_at + timedelta(
                    hours=random.randint(1, 72)
                )
                if is_completed
                else None
            )
        }

        # Add the action to the list.
        sales_actions.append(action)

        # Increase the action ID.
        action_id += 1


# Convert the generated records into a DataFrame.
sales_actions_df = pd.DataFrame(sales_actions)


# Create the output directory if needed.
os.makedirs(
    "database/synthetic_data/output",
    exist_ok=True
)


# Save the sales actions as a CSV file.
sales_actions_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# Display the first five records.
print(sales_actions_df.head())


# Display the total number of generated actions.
print(
    f"\nTotal sales actions generated: "
    f"{len(sales_actions_df)}"
)


# Display the average number of actions per lead.
print(
    f"Average sales actions per lead: "
    f"{len(sales_actions_df) / len(leads_df):.2f}"
)