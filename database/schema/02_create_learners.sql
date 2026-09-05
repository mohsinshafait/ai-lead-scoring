-- Create the learners table to store students
-- who may receive EduGrowth's educational services.
CREATE TABLE learners (

    -- Unique identifier for each learner.
    learner_id SERIAL PRIMARY KEY,

    -- Learner's first name.
    first_name VARCHAR(100) NOT NULL,

    -- Learner's last name.
    last_name VARCHAR(100) NOT NULL,

    -- Date of birth is stored instead of age because age changes over time.
    date_of_birth DATE,

    -- Current educational level of the learner.
    student_level VARCHAR(50) NOT NULL,

    -- Learner's city.
    city VARCHAR(100),

    -- Learner's country.
    country VARCHAR(100) NOT NULL,

    -- Timestamp when the learner record was created.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);