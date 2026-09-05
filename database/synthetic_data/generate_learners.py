# Import the required libraries.
import pandas as pd
import random
import os
from datetime import datetime, timedelta


# Set a random seed so that the generated data is reproducible.
random.seed(42)


# Number of learners we want to generate.
NUM_LEARNERS = 10000


# Define realistic Pakistani and international first names.
first_names = [
    "Ali", "Ahmed", "Hassan", "Hamza", "Usman",
    "Muhammad", "Abdullah", "Bilal", "Zain", "Saad",
    "Ayesha", "Fatima", "Maryam", "Hira", "Zainab",
    "Sara", "Noor", "Areeba", "Amna", "Iqra"
]


# Define last names for learners.
last_names = [
    "Khan", "Ahmed", "Malik", "Sheikh", "Butt",
    "Chaudhry", "Raza", "Hussain", "Ali", "Iqbal"
]


# Define the student levels supported by our course catalogue.
student_levels = [
    "Grade 6",
    "Grade 7",
    "Grade 8",
    "O Level",
    "IGCSE",
    "AS Level",
    "A Level"
]


# Define realistic age ranges for each educational level.
# The values represent the minimum and maximum learner age.
age_ranges = {
    "Grade 6": (10, 12),
    "Grade 7": (11, 13),
    "Grade 8": (12, 14),
    "O Level": (14, 17),
    "IGCSE": (14, 17),
    "AS Level": (16, 18),
    "A Level": (17, 20)
}


# Define the cities where learners are located.
cities = [
    "Lahore",
    "Karachi",
    "Islamabad",
    "Rawalpindi",
    "Faisalabad",
    "Multan",
    "Dubai",
    "Abu Dhabi",
    "London",
    "Riyadh"
]


# Define the countries corresponding to our target market.
countries = {
    "Lahore": "Pakistan",
    "Karachi": "Pakistan",
    "Islamabad": "Pakistan",
    "Rawalpindi": "Pakistan",
    "Faisalabad": "Pakistan",
    "Multan": "Pakistan",
    "Dubai": "UAE",
    "Abu Dhabi": "UAE",
    "London": "United Kingdom",
    "Riyadh": "Saudi Arabia"
}


# Define a function to generate a random date of birth
# based on the learner's educational level.
def generate_date_of_birth(student_level):
    """
    Generate a realistic date of birth based on the
    expected age range for a student level.
    """

    # Get the minimum and maximum age for the student level.
    min_age, max_age = age_ranges[student_level]

    # Randomly select an age from the allowed range.
    age = random.randint(min_age, max_age)

    # Use today's date as the reference point.
    today = datetime.today()

    # Estimate the birth date by subtracting the selected age.
    # A random number of additional days creates more variation.
    days_offset = random.randint(0, 364)

    return today - timedelta(
        days=(age * 365) + days_offset
    )


# Create an empty list to store learner records.
learners = []


# Generate the required number of learners.
for learner_id in range(1, NUM_LEARNERS + 1):

    # Randomly select the learner's educational level.
    student_level = random.choice(student_levels)

    # Randomly select a city.
    city = random.choice(cities)

    # Get the country based on the selected city.
    country = countries[city]

    # Generate the learner's date of birth.
    date_of_birth = generate_date_of_birth(student_level)

    # Generate the learner record.
    learner = {
        "learner_id": learner_id,
        "first_name": random.choice(first_names),
        "last_name": random.choice(last_names),
        "date_of_birth": date_of_birth.date(),
        "student_level": student_level,
        "city": city,
        "country": country,
        "created_at": datetime.now()
    }

    # Add the learner record to the list.
    learners.append(learner)


# Convert the generated learner records into a DataFrame.
learners_df = pd.DataFrame(learners)


# Create the output directory if it does not already exist.
os.makedirs(
    "database/synthetic_data/output",
    exist_ok=True
)


# Save the learner data as a CSV file.
learners_df.to_csv(
    "database/synthetic_data/output/learners.csv",
    index=False
)


# Display the first five generated learner records.
print(learners_df.head())


# Display the total number of generated learners.
print(f"\nTotal learners generated: {len(learners_df)}")