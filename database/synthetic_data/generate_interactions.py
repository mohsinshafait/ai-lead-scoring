# Import the required libraries.
import pandas as pd
import random
import os
from datetime import timedelta


# Set a random seed so that generated data is reproducible.
random.seed(42)


# Define the input and output file paths.
LEADS_PATH = "database/synthetic_data/output/leads.csv"
OUTPUT_PATH = "database/synthetic_data/output/interactions.csv"


# Load the previously generated leads.
leads_df = pd.read_csv(LEADS_PATH)


# Create an empty list to store interaction records.
interactions = []


# Start interaction IDs from 1.
interaction_id = 1


# Define interaction types for different engagement levels.
high_engagement_interactions = [
    "website_visit",
    "course_page_view",
    "pricing_page_view",
    "whatsapp_message",
    "trial_class_request",
    "phone_call",
]

medium_engagement_interactions = [
    "website_visit",
    "course_page_view",
    "pricing_page_view",
    "whatsapp_message",
    "email_inquiry",
]

low_engagement_interactions = [
    "website_visit",
    "course_page_view",
]


# Define the channel associated with each interaction type.
interaction_channels = {
    "website_visit": "Website",
    "course_page_view": "Website",
    "pricing_page_view": "Website",
    "whatsapp_message": "WhatsApp",
    "trial_class_request": "Website",
    "phone_call": "Phone",
    "email_inquiry": "Email",
}


# Define a function to assign an engagement level to a lead.
def generate_engagement_level():
    """
    Randomly assign an engagement level.

    Most leads are medium engagement, while fewer
    leads are high or low engagement.
    """

    return random.choices(
        ["High", "Medium", "Low"],
        weights=[0.25, 0.50, 0.25]
    )[0]


# Define a function to select interactions
# based on the lead's engagement level.
def generate_lead_interactions(engagement_level):
    """
    Generate realistic interactions based on
    the engagement level of a lead.
    """

    if engagement_level == "High":

        # High-engagement leads have more interactions.
        number_of_interactions = random.randint(4, 8)

        available_interactions = high_engagement_interactions

    elif engagement_level == "Medium":

        # Medium-engagement leads have a moderate number.
        number_of_interactions = random.randint(2, 5)

        available_interactions = medium_engagement_interactions

    else:

        # Low-engagement leads have fewer interactions.
        number_of_interactions = random.randint(1, 2)

        available_interactions = low_engagement_interactions

    # Randomly select the interaction types.
    return random.choices(
        available_interactions,
        k=number_of_interactions
    )


# Loop through every lead.
for _, lead in leads_df.iterrows():

    # Assign an engagement level.
    engagement_level = generate_engagement_level()

    # Generate interactions for this lead.
    lead_interactions = generate_lead_interactions(
        engagement_level
    )

    # Convert the lead creation time into a datetime object.
    lead_created_at = pd.to_datetime(
        lead["created_at"]
    )

    # Create one record for every interaction.
    for interaction_type in lead_interactions:

        # Generate the interaction after the lead was created.
        days_after_creation = random.randint(0, 90)

        interaction_time = lead_created_at + timedelta(
            days=days_after_creation,
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        # Create the interaction record.
        interaction = {
            "interaction_id": interaction_id,
            "lead_id": lead["lead_id"],
            "interaction_type": interaction_type,
            "interaction_channel": interaction_channels[
                interaction_type
            ],
            "interaction_details": (
                f"Synthetic {engagement_level.lower()} "
                f"engagement interaction"
            ),
            "interaction_at": interaction_time
        }

        # Add the interaction to the list.
        interactions.append(interaction)

        # Increase the interaction ID.
        interaction_id += 1


# Convert the interaction records into a DataFrame.
interactions_df = pd.DataFrame(interactions)


# Create the output directory if needed.
os.makedirs(
    "database/synthetic_data/output",
    exist_ok=True
)


# Save the interactions as a CSV file.
interactions_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# Display the first five interaction records.
print(interactions_df.head())


# Display the total number of interactions generated.
print(
    f"\nTotal interactions generated: "
    f"{len(interactions_df)}"
)


# Display the average interactions per lead.
print(
    f"Average interactions per lead: "
    f"{len(interactions_df) / len(leads_df):.2f}"
)