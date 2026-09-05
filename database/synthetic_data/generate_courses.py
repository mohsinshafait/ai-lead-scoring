# Import pandas to create and save the course data.
import pandas as pd


# Define the course catalogue.
# Each dictionary represents one educational product.
courses = [

    # Mathematics courses
    {
        "course_name": "Grade 6 Mathematics",
        "subject": "Mathematics",
        "student_level": "Grade 6",
        "learning_mode": "Online",
        "duration_weeks": 24,
        "price": 18000,
        "is_active": True,
    },
    {
        "course_name": "Grade 7 Mathematics",
        "subject": "Mathematics",
        "student_level": "Grade 7",
        "learning_mode": "Online",
        "duration_weeks": 24,
        "price": 20000,
        "is_active": True,
    },
    {
        "course_name": "Grade 8 Mathematics",
        "subject": "Mathematics",
        "student_level": "Grade 8",
        "learning_mode": "Online",
        "duration_weeks": 24,
        "price": 22000,
        "is_active": True,
    },

    # O Level and IGCSE Mathematics courses
    {
        "course_name": "O Level Mathematics",
        "subject": "Mathematics",
        "student_level": "O Level",
        "learning_mode": "Online",
        "duration_weeks": 36,
        "price": 30000,
        "is_active": True,
    },
    {
        "course_name": "IGCSE Mathematics",
        "subject": "Mathematics",
        "student_level": "IGCSE",
        "learning_mode": "Online",
        "duration_weeks": 36,
        "price": 35000,
        "is_active": True,
    },

    # Additional Mathematics courses
    {
        "course_name": "O Level Additional Mathematics",
        "subject": "Additional Mathematics",
        "student_level": "O Level",
        "learning_mode": "Online",
        "duration_weeks": 36,
        "price": 35000,
        "is_active": True,
    },
    {
        "course_name": "IGCSE Additional Mathematics",
        "subject": "Additional Mathematics",
        "student_level": "IGCSE",
        "learning_mode": "Online",
        "duration_weeks": 36,
        "price": 38000,
        "is_active": True,
    },

    # A Level Mathematics courses
    {
        "course_name": "AS Level Mathematics",
        "subject": "Mathematics",
        "student_level": "AS Level",
        "learning_mode": "Online",
        "duration_weeks": 40,
        "price": 45000,
        "is_active": True,
    },
    {
        "course_name": "A Level Mathematics",
        "subject": "Mathematics",
        "student_level": "A Level",
        "learning_mode": "Online",
        "duration_weeks": 40,
        "price": 50000,
        "is_active": True,
    },

    # Science courses
    {
        "course_name": "O Level Physics",
        "subject": "Physics",
        "student_level": "O Level",
        "learning_mode": "Online",
        "duration_weeks": 36,
        "price": 32000,
        "is_active": True,
    },
    {
        "course_name": "IGCSE Physics",
        "subject": "Physics",
        "student_level": "IGCSE",
        "learning_mode": "Online",
        "duration_weeks": 36,
        "price": 35000,
        "is_active": True,
    },
    {
        "course_name": "O Level Chemistry",
        "subject": "Chemistry",
        "student_level": "O Level",
        "learning_mode": "Online",
        "duration_weeks": 36,
        "price": 32000,
        "is_active": True,
    },
    {
        "course_name": "IGCSE Chemistry",
        "subject": "Chemistry",
        "student_level": "IGCSE",
        "learning_mode": "Online",
        "duration_weeks": 36,
        "price": 35000,
        "is_active": True,
    },
    {
        "course_name": "O Level Biology",
        "subject": "Biology",
        "student_level": "O Level",
        "learning_mode": "Online",
        "duration_weeks": 36,
        "price": 32000,
        "is_active": True,
    },
    {
        "course_name": "IGCSE Biology",
        "subject": "Biology",
        "student_level": "IGCSE",
        "learning_mode": "Online",
        "duration_weeks": 36,
        "price": 35000,
        "is_active": True,
    },

    # Computer Science courses
    {
        "course_name": "O Level Computer Science",
        "subject": "Computer Science",
        "student_level": "O Level",
        "learning_mode": "Online",
        "duration_weeks": 36,
        "price": 33000,
        "is_active": True,
    },
    {
        "course_name": "IGCSE Computer Science",
        "subject": "Computer Science",
        "student_level": "IGCSE",
        "learning_mode": "Online",
        "duration_weeks": 36,
        "price": 36000,
        "is_active": True,
    },

    # Business and Economics courses
    {
        "course_name": "O Level Business Studies",
        "subject": "Business",
        "student_level": "O Level",
        "learning_mode": "Online",
        "duration_weeks": 32,
        "price": 28000,
        "is_active": True,
    },
    {
        "course_name": "IGCSE Business Studies",
        "subject": "Business",
        "student_level": "IGCSE",
        "learning_mode": "Online",
        "duration_weeks": 32,
        "price": 30000,
        "is_active": True,
    },
    {
        "course_name": "O Level Economics",
        "subject": "Economics",
        "student_level": "O Level",
        "learning_mode": "Online",
        "duration_weeks": 32,
        "price": 30000,
        "is_active": True,
    },
    {
        "course_name": "IGCSE Economics",
        "subject": "Economics",
        "student_level": "IGCSE",
        "learning_mode": "Online",
        "duration_weeks": 32,
        "price": 32000,
        "is_active": True,
    },

    # English courses
    {
        "course_name": "O Level English",
        "subject": "English",
        "student_level": "O Level",
        "learning_mode": "Online",
        "duration_weeks": 32,
        "price": 28000,
        "is_active": True,
    },
    {
        "course_name": "IGCSE English",
        "subject": "English",
        "student_level": "IGCSE",
        "learning_mode": "Online",
        "duration_weeks": 32,
        "price": 30000,
        "is_active": True,
    },
]


# Convert the list of course dictionaries into a DataFrame.
courses_df = pd.DataFrame(courses)


# Add a course ID that will match the database identifier structure.
courses_df.index = range(1, len(courses_df) + 1)
courses_df.index.name = "course_id"


# Create the output directory if it does not already exist.
import os
os.makedirs("database/synthetic_data/output", exist_ok=True)


# Save the generated course data as a CSV file.
courses_df.to_csv(
    "database/synthetic_data/output/courses.csv"
)


# Display the generated data.
print(courses_df)


# Display the total number of generated courses.
print(f"\nTotal courses generated: {len(courses_df)}")