# Import the required libraries.
import pandas as pd
import random
import os
from datetime import datetime, timedelta


# Set a random seed so the generated data is reproducible.
random.seed(42)


# Define the number of leads to generate.
NUM_LEADS = 10000


# Define the input file paths.
COURSES_PATH = "database/synthetic_data/output/courses.csv"
LEARNERS_PATH = "database/synthetic_data/output/learners.csv"


# Load the previously generated courses and learners data.
courses_df = pd.read_csv(COURSES_PATH)
learners_df = pd.read_csv(LEARNERS_PATH)


# Define contact first names.
contact_first_names = [
    "Ali", "Ahmed", "Hassan", "Hamza", "Usman",
    "Muhammad", "Abdullah", "Bilal", "Zain", "Saad",
    "Ayesha", "Fatima", "Maryam", "Hira", "Zainab",
    "Sara", "Noor", "Areeba", "Amna", "Iqra"
]


# Define contact last names.
contact_last_names = [
    "Khan", "Ahmed", "Malik", "Sheikh", "Butt",
    "Chaudhry", "Raza", "Hussain", "Ali", "Iqbal"
]


# Define possible lead sources.
lead_sources = [
    "Google Search",
    "Facebook",
    "Instagram",
    "Referral",
    "Website",
    "WhatsApp",
    "YouTube"
]


# Define possible marketing campaigns.
campaigns = [
    "Organic",
    "Summer Campaign",
    "Exam Preparation Campaign",
    "Back to School Campaign",
    "Referral Campaign"
]


# Define the type of inquiry.
lead_types = [
    "Course Inquiry",
    "Free Consultation",
    "Trial Class",
    "Enrollment Inquiry"
]


# Define possible preferred contact methods.
contact_methods = [
    "WhatsApp",
    "Phone",
    "Email"
]


# Define possible lead statuses.
# These represent the current stage of the lead.
lead_statuses = [
    "New",
    "Contacted",
    "Qualified",
    "Follow-up",
    "Closed"
]


# Define countries with different approximate purchasing power.
country_budget_factor = {
    "Pakistan": 1.0,
    "UAE": 1.5,
    "United Kingdom": 2.0,
    "Saudi Arabia": 1.4
}


# Create a function to generate a realistic lead budget.
def generate_budget(course_price, country):
    """
    Generate a budget based on the course price,
    country, and some realistic random variation.
    """

    # Get the purchasing power factor for the country.
    factor = country_budget_factor.get(country, 1.0)

    # Generate a random variation around the course price.
    variation = random.uniform(0.6, 1.3)

    # Calculate the estimated budget.
    budget = course_price * factor * variation

    # Round the budget to two decimal places.
    return round(budget, 2)


# Create a function to generate a realistic decision maker.
def generate_decision_maker(student_level):
    """
    Younger learners are more likely to have
    a parent as the decision-maker.
    """

    # School and O Level students are usually represented by parents.
    if student_level in ["Grade 6", "Grade 7", "Grade 8", "O Level", "IGCSE"]:
        return random.choices(
            ["Parent", "Learner"],
            weights=[0.85, 0.15]
        )[0]

    # Older learners have a higher chance of making their own decisions.
    return random.choices(
        ["Parent", "Learner"],
        weights=[0.40, 0.60]
    )[0]


# Create a function to generate a random lead creation date.
def generate_created_at():
    """
    Generate a lead creation timestamp within
    the last 12 months.
    """

    # Use the current date as the reference point.
    current_date = datetime.now()

    # Select a random number of days in the last year.
    days_ago = random.randint(0, 365)

    # Select a random number of seconds during the day.
    seconds = random.randint(0, 86399)

    # Return the generated timestamp.
    return current_date - timedelta(
        days=days_ago,
        seconds=seconds
    )


# Create an empty list to store lead records.
leads = []


# Generate the required number of leads.
for lead_id in range(1, NUM_LEADS + 1):

    # Select a learner from the learners dataset.
    learner = learners_df.sample(
        n=1,
        random_state=None
    ).iloc[0]

    # Get the learner's educational level.
    student_level = learner["student_level"]

    # Find courses that match the learner's educational level.
    matching_courses = courses_df[
        courses_df["student_level"] == student_level
    ]

    # Select one course from the matching courses.
    course = matching_courses.sample(
        n=1
    ).iloc[0]

    # Generate the decision-maker based on learner level.
    decision_maker = generate_decision_maker(student_level)

    # Generate the lead record.
    lead = {
        "lead_id": lead_id,
        "learner_id": learner["learner_id"],
        "course_id": course["course_id"],

        # Generate contact details.
        "contact_first_name": random.choice(contact_first_names),
        "contact_last_name": random.choice(contact_last_names),

        # Generate a synthetic email address.
        "email": (
            f"lead{lead_id}"
            f"@example.com"
        ),

        # Generate a synthetic phone number.
        "phone": (
            f"+92-3{random.randint(10, 49)}"
            f"{random.randint(1000000, 9999999)}"
        ),

        # Business and marketing information.
        "decision_maker_type": decision_maker,
        "lead_source": random.choice(lead_sources),
        "campaign": random.choice(campaigns),
        "lead_type": random.choice(lead_types),
        "preferred_contact_method": random.choice(contact_methods),

        # Generate the budget based on the selected course
        # and learner location.
        "budget": generate_budget(
            course["price"],
            learner["country"]
        ),

        # Assign an initial lead status.
        "lead_status": random.choice(lead_statuses),

        # Generate the lead creation timestamp.
        "created_at": generate_created_at()
    }

    # Add the lead to the list.
    leads.append(lead)


# Convert the generated lead records into a DataFrame.
leads_df = pd.DataFrame(leads)


# Create the output directory if it does not already exist.
os.makedirs(
    "database/synthetic_data/output",
    exist_ok=True
)


# Save the generated leads data.
leads_df.to_csv(
    "database/synthetic_data/output/leads.csv",
    index=False
)


# Display the first five lead records.
print(leads_df.head())


# Display the total number of generated leads.
print(f"\nTotal leads generated: {len(leads_df)}")